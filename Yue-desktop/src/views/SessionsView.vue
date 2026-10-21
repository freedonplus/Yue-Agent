<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { listSessions, deleteSession, createSession } from "../api/resources";
import { useChat } from "../composables/useChat";
import CButton from "../base/CButton.vue";
import CCard from "../base/CCard.vue";
import CInput from "../base/CInput.vue";
import CTag from "../base/CTag.vue";
import CModal from "../base/CModal.vue";
import CEmpty from "../base/CEmpty.vue";
import CLoading from "../base/CLoading.vue";

const router = useRouter();
const { loadSession } = useChat();

const sessions = ref([]);
const loading = ref(false);
const q = ref("");
const confirmId = ref(null);
const showCreate = ref(false);
const newTitle = ref("");
const errMsg = ref("");

async function fetchSessions() {
  loading.value = true;
  errMsg.value = "";
  try {
    sessions.value = await listSessions({ q: q.value, limit: 200 });
  } catch (e) {
    errMsg.value = e.message || "加载会话失败";
    sessions.value = [];
  } finally {
    loading.value = false;
  }
}

function open(sid) {
  router.push("/chat");
  loadSession(sid);
}

function askDelete(sid) {
  confirmId.value = sid;
}
async function doDelete() {
  if (!confirmId.value) return;
  try {
    await deleteSession(confirmId.value);
    confirmId.value = null;
    await fetchSessions();
  } catch (e) {
    errMsg.value = e.message || "删除失败（可能需管理员权限）";
    confirmId.value = null;
  }
}
async function doCreate() {
  if (!newTitle.value.trim()) return;
  try {
    const s = await createSession({ title: newTitle.value.trim() });
    showCreate.value = false;
    newTitle.value = "";
    await fetchSessions();
    if (s?.session_id) open(s.session_id);
  } catch (e) {
    errMsg.value = e.message || "创建失败";
  }
}

function fmtTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleString("zh-CN", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
}

onMounted(fetchSessions);
</script>

<template>
  <div class="page">
    <div class="page__head">
      <h2 class="c-section-title">会话记录</h2>
      <div class="row gap-2 grow">
        <CInput v-model="q" placeholder="搜索标题 / 最近消息" @keydown.enter="fetchSessions" />
        <CButton type="white" @click="fetchSessions">搜索</CButton>
        <CButton type="green" @click="showCreate = true">新建会话</CButton>
      </div>
    </div>

    <CLoading v-if="loading" text="加载会话…" />
    <div v-else-if="errMsg && !sessions.length" class="c-card page__err">
      <CTag type="red">出错</CTag>
      <span class="comic-text">{{ errMsg }}</span>
    </div>
    <CEmpty v-else-if="!sessions.length" title="还没有会话" desc="去对话页开一个新会话吧">
      <CButton type="red" @click="router.push('/chat')">去对话</CButton>
    </CEmpty>

    <div v-else class="session-grid">
      <CCard v-for="s in sessions" :key="s.id" class="session-card group" @click="open(s.session_id)">
        <div class="row gap-2">
          <div class="grow">
            <div class="comic-title session-title text-ellipsis">{{ s.title || "未命名会话" }}</div>
            <div class="comic-muted session-msg text-ellipsis">{{ s.last_message || "（空）" }}</div>
          </div>
          <span class="c-pop-tag"><CTag type="yellow">{{ s.message_count }} 条</CTag></span>
        </div>
        <div class="row gap-2 session-meta">
          <CTag type="white">{{ fmtTime(s.updated_at || s.created_at) }}</CTag>
          <span class="spacer"></span>
          <button class="session-del" @click.stop="askDelete(s.session_id)" title="删除会话">删除</button>
        </div>
      </CCard>
    </div>

    <!-- 删除确认 -->
    <CModal :model-value="!!confirmId" @update:model-value="(v) => v || (confirmId = null)" title="删除会话?">
      <p class="comic-text">确定删除该会话及其全部消息？此操作不可恢复。</p>
      <template #footer>
        <CButton type="ghost" @click="confirmId = null">取消</CButton>
        <CButton type="red" @click="doDelete">确认删除</CButton>
      </template>
    </CModal>

    <!-- 新建 -->
    <CModal :model-value="showCreate" @update:model-value="(v) => (showCreate = v)" title="新会话">
      <CInput v-model="newTitle" placeholder="会话标题" @keydown.enter="doCreate" />
      <template #footer>
        <CButton type="ghost" @click="showCreate = false">取消</CButton>
        <CButton type="green" @click="doCreate">创建</CButton>
      </template>
    </CModal>
  </div>
</template>

<style scoped>
.page { padding: 18px; display: flex; flex-direction: column; gap: 16px; height: 100%; overflow-y: auto; }
.page__head { display: flex; flex-direction: column; gap: 10px; }
.page__head .c-input { max-width: 420px; }
.page__err { padding: 14px; display: flex; gap: 10px; align-items: center; }
.session-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.session-card { padding: 14px; cursor: pointer; }
.session-card:hover { transform: translate(-2px, -2px); box-shadow: var(--shadow-hover); }
.session-title { font-size: 15px; }
.session-msg { font-size: 12px; margin-top: 4px; }
.session-meta { margin-top: 10px; }
.session-del {
  border: 2px solid var(--ink);
  background: #fff;
  font-weight: 700;
  font-size: 12px;
  padding: 2px 8px;
  cursor: pointer;
}
.session-del:hover { background: var(--red); color: #fff; transform: scale(1.05) rotate(-2deg); }
</style>
