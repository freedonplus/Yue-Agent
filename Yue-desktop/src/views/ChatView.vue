<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useChat } from "../composables/useChat";
import { listSkillSummary } from "../api/resources";
import CButton from "../base/CButton.vue";
import CTextarea from "../base/CTextarea.vue";
import CTag from "../base/CTag.vue";
import CBubble from "../base/CBubble.vue";
import CModal from "../base/CModal.vue";
import CMarkdown from "../base/CMarkdown.vue";
import CLoading from "../base/CLoading.vue";
import CEmpty from "../base/CEmpty.vue";
import yueIcon from "../assets/yue-icon.svg";

const {
  messages,
  currentSessionId,
  running,
  waitingApproval,
  pendingApprovals,
  approvals,
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
} = useChat();

const draft = ref("");
const showSkills = ref(false);
const showParams = ref(false);
const skills = ref([]);
const skillLoaded = ref(false);
const approvalMessage = ref("");
const listRef = ref(null);

// 输入框自动高度
function autosize(e) {
  e.target.style.height = "auto";
  e.target.style.height = Math.min(e.target.scrollHeight, 180) + "px";
}

function onInput(e) {
  draft.value = e.target.value;
  autosize(e);
}

async function submit() {
  const text = draft.value.trim();
  if (!text || running.value) return;
  draft.value = "";
  await send(text);
  scrollBottom();
}

function onKeydown(e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    submit();
  }
}

function scrollBottom() {
  nextTick(() => {
    listRef.value?.scrollTo({ top: listRef.value.scrollHeight, behavior: "smooth" });
  });
}

async function loadSkills() {
  try {
    skills.value = await listSkillSummary();
    skillLoaded.value = true;
  } catch {
    skills.value = [];
    skillLoaded.value = true;
  }
}

function pickSkill(slug) {
  skillSlug.value = skillSlug.value === slug ? "" : slug;
  showSkills.value = false;
}

// 审批：通过 / 拒绝
function approve(approval) {
  decide(approval, "approve");
}
function reject(approval) {
  decide(approval, "reject", approvalMessage.value || "用户拒绝");
}
function rejectAll() {
  approvals.value
    .filter((a) => a.decision === null)
    .forEach((a) => decide(a, "reject", approvalMessage.value || "用户拒绝"));
}

onMounted(async () => {
  await loadSkills();
  scrollBottom();
});
</script>

<template>
  <div class="chat">
    <!-- 头部：会话状态 -->
    <header class="chat__head">
      <div class="row gap-3 grow">
        <span class="c-dot" :class="running ? 'c-dot--online' : 'c-dot--offline'"></span>
        <span class="comic-title chat__head-title">YUE CHAT</span>
        <CTag v-if="running" type="red">运行中</CTag>
        <CTag v-if="currentSessionId" type="white" class="text-ellipsis chat__head-sid">{{ currentSessionId }}</CTag>
      </div>
      <div v-if="running" class="row gap-2">
        <CTag type="blue">节点: {{ currentNode ? nodeName(currentNode) : "…" }}</CTag>
        <CButton size="sm" type="red" @click="cancel">停止</CButton>
      </div>
    </header>

    <!-- 消息区 -->
    <div ref="listRef" class="chat__list">
      <template v-if="messages.length">
        <div
          v-for="(m, idx) in messages"
          :key="idx"
          class="chat__row"
          :class="m.role === 'user' ? 'chat__row--user' : 'chat__row--bot'"
        >
          <template v-if="m.role === 'user'">
            <CBubble side="user">{{ m.content }}</CBubble>
          </template>
          <template v-else>
            <div class="chat__bot-head row gap-2">
              <span class="c-dot c-dot--online"></span>
              <span class="comic-title chat__bot-name">{{ m.name || "Yue" }}</span>
            </div>
            <!-- 工具调用过程 -->
            <div v-if="m.toolCalls.length" class="chat__tools">
              <div v-for="(tc, ti) in m.toolCalls" :key="ti" class="chat__tool row gap-2">
                <CTag type="blue">{{ tc.name }}</CTag>
                <code class="chat__tool-args">{{ JSON.stringify(tc.args) }}</code>
              </div>
            </div>
            <!-- 正文 -->
            <CBubble side="bot">
              <CMarkdown v-if="m.content" :content="m.content" />
              <CLoading v-if="m.pending && !m.content" text="思考中…" />
            </CBubble>
          </template>
        </div>
      </template>

      <!-- 空状态 -->
      <CEmpty
        v-else-if="!errorMsg"
        title="向 Yue 提问"
        desc="我可以读代码、查资料、写文档、处理表格与文件。输入你的需求开始吧。"
        :icon="yueIcon"
      />

      <!-- 错误 -->
      <div v-if="errorMsg" class="chat__error c-card">
        <CTag type="red">出错</CTag>
        <span class="comic-text">{{ errorMsg }}</span>
        <span v-if="!currentSessionId" class="comic-muted">（后端未连接或尚未配置 AUTH_TOKEN）</span>
      </div>
    </div>

    <!-- 节点轨迹 -->
    <div v-if="nodePath.length" class="chat__trace">
      <span class="comic-muted">路径:</span>
      <CTag v-for="(n, i) in nodePath" :key="i" type="white">{{ nodeName(n) }}</CTag>
    </div>

    <!-- 技能选择器 -->
    <div class="chat__skillbar row gap-2">
      <CTag :type="skillSlug ? 'green' : 'white'">
        {{ skillSlug ? "技能: " + skillSlug : "技能: 自动" }}
      </CTag>
      <CButton size="sm" type="ghost" @click="showSkills = !showSkills">选择技能</CButton>
      <div v-if="workdir" class="chat__workdir text-ellipsis comic-muted">{{ workdir }}</div>
    </div>
    <div v-if="showSkills" class="chat__skills">
      <div class="row gap-2 wrap">
        <CButton size="sm" type="ghost" @click="pickSkill('')">自动判断</CButton>
        <CButton
          v-for="s in skills"
          :key="s.id"
          size="sm"
          :type="skillSlug === s.slug ? 'green' : 'ghost'"
          @click="pickSkill(s.slug)"
        >
          {{ s.name || s.slug }}
        </CButton>
        <span v-if="!skills.length && skillLoaded" class="comic-muted">（暂无技能，或后端未连接）</span>
      </div>
    </div>

    <!-- 输入区（豆包式：卡片内嵌输入框 + 右下角发送） -->
    <div class="chat__input">
      <div class="chat__composer">
        <textarea
          class="chat__composer-textarea"
          :value="draft"
          placeholder="输入消息，Enter 发送，Shift+Enter 换行"
          @input="onInput"
          @keydown="onKeydown"
          rows="1"
        ></textarea>
        <div class="chat__composer-bar">
          <!-- 工作区选择 -->
          <select v-model="workdir" class="chat__workspace" title="工作目录" aria-label="工作目录">
            <option value="">工作区: 默认</option>
            <option value="C:/Users/tzy88/Desktop/Yue Agent">Yue Agent</option>
            <option value="C:/Users/tzy88/Desktop">Desktop</option>
          </select>
          <!-- 模型参数 -->
          <button class="chat__param-btn" @click="showParams = !showParams" title="模型参数" aria-label="模型参数">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <circle cx="12" cy="12" r="3" />
              <path d="M12 1v4 M12 19v4 M4.2 4.2l2.8 2.8 M17 17l2.8 2.8 M1 12h4 M19 12h4 M4.2 19.8l2.8-2.8 M17 7l2.8-2.8" />
            </svg>
            参数
          </button>
          <!-- token 统计 -->
          <span v-if="totalTokens > 0" class="chat__tokens comic-muted" title="累计 token 用量">
            TOKEN {{ totalTokens }}
          </span>
          <span class="spacer"></span>
          <span class="chat__composer-hint comic-muted">Enter 发送</span>
          <button
            v-if="!running"
            class="chat__send"
            :disabled="!draft.trim()"
            @click="submit"
            aria-label="发送"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M22 2 L11 13" />
              <path d="M22 2 L15 22 L11 13 L2 9 Z" />
            </svg>
            <span>发送</span>
          </button>
          <button v-else class="chat__send chat__send--stop" @click="cancel">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <rect x="5" y="5" width="14" height="14" />
            </svg>
            <span>停止</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 模型参数面板 -->
    <div v-if="showParams" class="chat__params c-card">
      <div class="chat__params-title comic-title">模型参数</div>
      <div class="row gap-3 wrap">
        <div>
          <label class="comic-muted chat__params-label">温度 temperature</label>
          <input
            class="c-input chat__params-input"
            v-model="modelParams.temperature"
            type="number"
            step="0.1"
            min="0"
            max="2"
            placeholder="默认 0.7"
          />
        </div>
        <div>
          <label class="comic-muted chat__params-label">最大输出 max_tokens</label>
          <input
            class="c-input chat__params-input"
            v-model="modelParams.max_tokens"
            type="number"
            step="1"
            min="1"
            placeholder="默认 4096"
          />
        </div>
      </div>
      <p class="comic-muted chat__params-hint">
        留空使用后端默认值；这些参数随对话请求发送，需后端在 /api/chat/stream 支持。
      </p>
    </div>

    <!-- 审批弹窗 -->
    <CModal :model-value="waitingApproval" @update:model-value="() => {}" title="需要审批!" width="560px">
      <p class="comic-text">以下操作需要你确认：</p>
      <div class="approval-list">
        <div v-for="(a, i) in pendingApprovals" :key="i" class="approval-item c-card">
          <div class="row gap-2 wrap">
            <CTag type="blue">{{ a.tool }}</CTag>
            <code class="chat__tool-args">{{ JSON.stringify(a.args) }}</code>
          </div>
          <p v-if="a.description" class="comic-muted approval-desc">{{ a.description }}</p>
          <div class="row gap-2 wrap approval-actions">
            <CButton size="sm" type="green" @click="approve(a)">批准</CButton>
            <CButton size="sm" type="red" @click="reject(a)">拒绝</CButton>
          </div>
        </div>
      </div>
      <div class="row gap-2 approval-reject-all">
        <CTextarea
          :model-value="approvalMessage"
          @update:model-value="(v) => (approvalMessage = v)"
          placeholder="拒绝理由（可选）"
          :rows="2"
        />
        <CButton type="ghost" @click="rejectAll">全部拒绝</CButton>
      </div>
      <div v-if="!pendingApprovals.length" class="comic-muted">处理中，请稍候…</div>
    </CModal>
  </div>
</template>

<style scoped>
.chat {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.chat__head {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  background: var(--paper);
  border-bottom: 4px solid var(--ink);
}
.chat__head-title { font-size: 18px; }
.chat__head-sid { max-width: 200px; }
.chat__list {
  flex: 1;
  overflow-y: auto;
  padding: 18px 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.chat__row { display: flex; flex-direction: column; }
.chat__row--user { align-items: flex-end; }
.chat__row--bot { align-items: flex-start; }
.chat__bot-head { margin-bottom: 6px; padding-left: 6px; }
.chat__bot-name { font-size: 13px; color: var(--blue); }
.chat__tools { margin: 0 0 8px 6px; display: flex; flex-direction: column; gap: 6px; }
.chat__tool { align-items: flex-start; }
.chat__tool-args {
  font-family: var(--mono);
  font-size: 11px;
  background: #fff;
  border: 2px solid var(--ink);
  padding: 2px 6px;
  max-width: 100%;
  overflow-x: auto;
}
.chat__error {
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.chat__trace {
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  border-top: 2px solid var(--ink);
}
.chat__skillbar {
  padding: 8px 16px;
  border-top: 3px solid var(--ink);
  background: var(--paper);
  flex-wrap: wrap;
}
.chat__workdir { max-width: 240px; font-size: 12px; }
.chat__skills {
  padding: 8px 16px;
  background: #fff;
  border-top: 2px solid var(--ink);
}
.chat__input {
  padding: 10px 16px 14px;
  border-top: 4px solid var(--ink);
  background: var(--paper);
}
/* 豆包式输入卡片 */
.chat__composer {
  background: #fff;
  border: 4px solid var(--ink);
  box-shadow: var(--shadow-sm);
  padding: 12px 14px 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: box-shadow 0.12s, transform 0.12s;
}
.chat__composer:focus-within {
  box-shadow: var(--shadow);
  transform: translate(-1px, -1px);
}
.chat__composer-textarea {
  width: 100%;
  border: none;
  outline: none;
  resize: none;
  font-family: inherit;
  font-size: 14px;
  font-weight: 600;
  color: var(--ink);
  background: transparent;
  line-height: 1.5;
  max-height: 180px;
}
.chat__composer-textarea::placeholder { color: #9c9c8a; font-weight: 700; }
.chat__composer-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  border-top: 2px dashed var(--ink);
  padding-top: 6px;
}
.chat__composer-hint { font-size: 11px; white-space: nowrap; }
/* 工作区下拉 */
.chat__workspace {
  border: 2px solid var(--ink);
  background: var(--paper);
  font-family: inherit;
  font-size: 12px;
  font-weight: 700;
  color: var(--ink);
  padding: 4px 6px;
  max-width: 170px;
  cursor: pointer;
}
.chat__workspace:focus { outline: 2px dashed var(--ink); outline-offset: 1px; }
/* 参数按钮 */
.chat__param-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  border: 2px solid var(--ink);
  background: #fff;
  font-family: inherit;
  font-size: 12px;
  font-weight: 900;
  color: var(--ink);
  padding: 4px 8px;
  cursor: pointer;
  transition: transform 0.1s, background-color 0.1s;
}
.chat__param-btn:hover { background: var(--yellow); transform: scale(1.06) rotate(-2deg); }
.chat__param-btn:active { transform: translate(2px, 2px); }
/* token 徽标 */
.chat__tokens {
  font-size: 11px;
  border: 2px solid var(--ink);
  background: #fff;
  padding: 3px 8px;
  font-weight: 900;
  white-space: nowrap;
}
/* 模型参数面板 */
.chat__params {
  margin: 0 16px 8px;
  padding: 12px 14px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.chat__params-title { font-size: 13px; }
.chat__params-label { display: block; margin-bottom: 5px; font-size: 12px; }
.chat__params-input { width: 160px; }
.chat__params-hint { margin: 0; font-size: 11px; }
.chat__send {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border: 3px solid var(--ink);
  background: var(--yellow);
  color: var(--ink);
  font-weight: 900;
  font-size: 13px;
  text-transform: uppercase;
  cursor: pointer;
  box-shadow: 3px 3px 0 0 var(--ink);
  transition: transform 0.1s, box-shadow 0.1s, background-color 0.1s, color 0.1s;
}
.chat__send:hover { transform: scale(1.08) rotate(-3deg); box-shadow: 5px 5px 0 0 var(--ink); background: var(--red); color: #fff; }
.chat__send:active { transform: translate(3px, 3px); box-shadow: none; }
.chat__send:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: 2px 2px 0 0 var(--ink);
}
.chat__send--stop { background: var(--red); color: #fff; }
.chat__send--stop:hover { background: var(--ink); color: var(--yellow); }
.chat__input-actions { justify-content: flex-end; }
.approval-list { display: flex; flex-direction: column; gap: 10px; margin: 12px 0; }
.approval-item { padding: 12px; display: flex; flex-direction: column; gap: 8px; }
.approval-desc { margin: 0; font-size: 12px; }
.approval-actions { justify-content: flex-end; }
.approval-reject-all { gap: 10px; align-items: flex-start; }
</style>
