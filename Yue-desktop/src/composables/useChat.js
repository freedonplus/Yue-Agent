// ============================================================
// useChat —— 核心对话状态机
// 处理 SSE 事件（node/reasoning/token/tool_call/approval_required/
// done/error），支持审批续跑（/api/chat/approve）。
// 模块级单例：ChatView / SessionsView 共享同一份会话状态。
// ============================================================
import { reactive, ref, computed } from "vue";
import { consumeStream } from "../api/chat";
import { listSessions, createSession, getSessionMessages } from "../api/resources";

const messages = ref([]);       // {role, content, name, toolCalls, pending}
const currentSessionId = ref(null);
const running = ref(false);
const waitingApproval = ref(false);
const approvals = ref([]);      // [{interrupt_id, tool_call_id, tool, args, description, decision, message}]
const runId = ref(null);
const errorMsg = ref("");
const nodePath = ref([]);       // 本轮访问过的节点
const currentNode = ref(null);
const skillSlug = ref("");
const workdir = ref("");
const user_id = ref("default");
const modelParams = reactive({   // 模型参数（后端支持后生效）
  temperature: null,
  max_tokens: null,
});
const totalTokens = ref(0);      // 累计 token（依赖后端 usage 事件）
const abortCtrl = ref(null);

let resumeResolve = null;
let lastAssistantIndex = -1;

// 员工 slug -> 中文名（从 AGENTS.md 已知，动态拉取可覆盖）
const ROLE_NAMES = {
  worker_yue_chat: "Yue 输出管卡",
  supervisor: "调度员",
  worker_files: "文件员工",
  worker_research: "研究员",
  worker_writer: "写手",
  worker_coder: "代码工程师",
  worker_browser: "浏览器操作员",
  worker_data: "数据分析师",
  worker_docs: "文档专员",
  worker_news: "资讯员",
  worker_planner: "规划师",
  worker_frontend: "前端工程师",
  worker_life: "生活助手",
};

function nodeName(slug) {
  return ROLE_NAMES[slug] || slug;
}

// 累加 token 用量（后端 usage 事件可能带 input_tokens/output_tokens/total_tokens）
function accumulateUsage(evt) {
  const u = evt.usage || evt;
  const add = Number(u.total_tokens ?? u.total ?? 0) ||
    (Number(u.input_tokens ?? 0) + Number(u.output_tokens ?? 0));
  if (add) totalTokens.value += add;
}

function makeAssistant() {
  const m = reactive({ role: "assistant", content: "", toolCalls: [], pending: true, name: null });
  messages.value.push(m);
  return m;
}

// 把 messages 转成 history（只保留 user / assistant 最终内容，最多 50 条）
function toHistory() {
  const h = [];
  for (const m of messages.value) {
    if (m.role === "user") {
      h.push({ role: "user", content: m.content });
    } else if (m.role === "assistant") {
      h.push({ role: "assistant", content: m.content || "…" });
    }
    if (h.length >= 50) break;
  }
  return h;
}

function handleEvent(evt, assistant) {
  switch (evt.type) {
    case "node":
      currentNode.value = evt.node;
      if (!nodePath.value.includes(evt.node)) nodePath.value.push(evt.node);
      break;
    case "reasoning":
      // 前端不展示思考过程，只忽略（后端仍需发送则忽略即可）
      break;
    case "token":
      assistant.content += evt.content || "";
      break;
    case "tool_call": {
      const list = evt.tool_calls || [];
      assistant.toolCalls = list.map((tc) => ({
        id: tc.id || tc.tool_call_id || "",
        name: tc.name || tc.tool || "",
        args: tc.args || {},
      }));
      break;
    }
    case "usage":
      // 后端新增：单轮用量统计
      accumulateUsage(evt);
      break;
    case "approval_required":
      runId.value = evt.run_id || runId.value;
      approvals.value = (evt.approvals || []).map((a) => ({
        interrupt_id: a.interrupt_id,
        tool_call_id: a.tool_call_id,
        tool: a.tool,
        args: a.args || {},
        description: a.description || "",
        decision: null,       // approve | reject | null
        message: "",
      }));
      waitingApproval.value = approvals.value.length > 0;
      break;
    case "done":
      if (evt.content) assistant.content = evt.content;
      assistant.pending = false;
      if (evt.run_id) runId.value = evt.run_id;
      if (evt.paused) {
        // 停在审批：waitingApproval 由 approval_required 维护
      } else {
        waitingApproval.value = false;
        approvals.value = [];
      }
      break;
    case "error":
      errorMsg.value = evt.message || "运行失败";
      assistant.pending = false;
      break;
    default:
      break;
  }
}

async function ensureSession(title) {
  if (currentSessionId.value) return currentSessionId.value;
  const sid = `s-${Date.now()}`;
  try {
    await createSession({ session_id: sid, title: title.slice(0, 30) || "新会话", workdir: workdir.value });
    currentSessionId.value = sid;
  } catch (e) {
    if (e.code === "SESSION_EXISTS") {
      currentSessionId.value = sid;
    } else {
      // 创建失败也继续对话（后端可能自动记录）
      currentSessionId.value = sid;
    }
  }
  return sid;
}

async function send(text) {
  if (running.value || !text.trim()) return;
  running.value = true;
  errorMsg.value = "";
  nodePath.value = [];
  currentNode.value = null;
  abortCtrl.value = new AbortController();

  messages.value.push({ role: "user", content: text.trim(), pending: false });
  const assistant = makeAssistant();

  try {
    const sid = await ensureSession(text.trim());
    const base = {
      session_id: sid,
      workdir: workdir.value,
      skill_slug: skillSlug.value || undefined,
      user_id: user_id.value || "default",
      // 模型参数（后端支持后生效）
      ...(modelParams.temperature !== null && modelParams.temperature !== undefined
        ? { temperature: Number(modelParams.temperature) }
        : {}),
      ...(modelParams.max_tokens !== null && modelParams.max_tokens !== undefined && modelParams.max_tokens !== ""
        ? { max_tokens: Number(modelParams.max_tokens) }
        : {}),
    };

    // 主循环：发起 -> 审批 -> 续跑（可多轮审批）
    for (;;) {
      const payload = { ...base, message: text.trim(), history: toHistory() };
      await consumeStream(
        "/chat/stream",
        payload,
        (evt) => handleEvent(evt, assistant),
        { signal: abortCtrl.value.signal }
      );

      // 有待审批：等待用户决策
      if (approvals.value.some((a) => a.decision === null)) {
        waitingApproval.value = true;
        await new Promise((resolve) => {
          resumeResolve = resolve;
          // 若被取消则立即放行
          if (abortCtrl.value.signal.aborted) resolve();
        });
        if (abortCtrl.value.signal.aborted) break;
        waitingApproval.value = false;
      } else {
        break; // 无待审批，结束
      }

      // 提交审批并续跑
      const decisions = approvals.value.map((a) => ({
        interrupt_id: a.interrupt_id,
        type: a.decision,
        ...(a.message ? { message: a.message } : {}),
      }));
      approvals.value = [];
      await consumeStream(
        "/chat/approve",
        { ...base, run_id: runId.value, decisions },
        (evt) => handleEvent(evt, assistant),
        { signal: abortCtrl.value.signal }
      );
    }
  } catch (e) {
    if (e.name === "AbortError") {
      errorMsg.value = "已停止";
    } else {
      errorMsg.value = e.message || "请求失败";
      // 网络失败时标记 assistant 完成，避免一直 pending
      assistant.pending = false;
    }
  } finally {
    running.value = false;
    currentNode.value = null;
    resumeResolve = null;
    abortCtrl.value = null;
  }
}

function cancel() {
  if (abortCtrl.value) abortCtrl.value.abort();
  if (resumeResolve) resumeResolve();
}

function decide(approval, decision, message = "") {
  approval.decision = decision;
  approval.message = message;
  if (approvals.value.every((a) => a.decision !== null)) {
    // 全部决策完成：解除等待
    if (resumeResolve) {
      const r = resumeResolve;
      resumeResolve = null;
      r();
    }
  }
}

function reset() {
  cancel();
  messages.value = [];
  currentSessionId.value = null;
  approvals.value = [];
  waitingApproval.value = false;
  errorMsg.value = "";
  nodePath.value = [];
  currentNode.value = null;
  runId.value = null;
  totalTokens.value = 0;
}

// 载入既有会话消息（重新打开会话时回放）
async function loadSession(sessionId) {
  cancel();
  messages.value = [];
  currentSessionId.value = sessionId;
  approvals.value = [];
  waitingApproval.value = false;
  errorMsg.value = "";
  try {
    const list = await getSessionMessages(sessionId, { limit: 200 });
    messages.value = (list || []).map((m) => ({
      role: m.role,
      content: m.content || "",
      name: m.name || null,
      pending: false,
      toolCalls: [],
    }));
  } catch (e) {
    errorMsg.value = e.message || "加载会话失败";
  }
}

async function newSession() {
  reset();
  // 拉一份会话列表给侧栏用
  const list = await listSessions({ limit: 20 }).catch(() => []);
  return list;
}

const pendingApprovals = computed(() => approvals.value.filter((a) => a.decision === null));

export function useChat() {
  return {
    messages,
    currentSessionId,
    running,
    waitingApproval,
    approvals,
    pendingApprovals,
    runId,
    errorMsg,
    nodePath,
    currentNode,
    skillSlug,
    workdir,
    user_id,
    modelParams,
    totalTokens,
    nodeName,
    send,
    cancel,
    decide,
    reset,
    loadSession,
    newSession,
    ensureSession,
    toHistory,
  };
}
