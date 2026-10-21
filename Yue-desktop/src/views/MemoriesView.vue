<script setup>
import { ref, onMounted } from "vue";
import { listMemories, createMemory, deleteMemory } from "../api/resources";
import { useChat } from "../composables/useChat";
import CButton from "../base/CButton.vue";
import CCard from "../base/CCard.vue";
import CInput from "../base/CInput.vue";
import CTextarea from "../base/CTextarea.vue";
import CTag from "../base/CTag.vue";
import CModal from "../base/CModal.vue";
import CEmpty from "../base/CEmpty.vue";
import CLoading from "../base/CLoading.vue";

const { user_id } = useChat();

const memories = ref([]);
const loading = ref(false);
const q = ref("");
const errMsg = ref("");
const showAdd = ref(false);
const newContent = ref("");
const newKind = ref("fact");
const newTags = ref("");
const confirmId = ref(null);

const KINDS = [
  { value: "profile", label: "画像" },
  { value: "preference", label: "偏好" },
  { value: "decision", label: "决策" },
  { value: "fact", label: "事实" },
];

function kindLabel(k) {
  return KINDS.find((x) => x.value === k)?.label || k;
}
function kindType(k) {
  return { profile: "blue", preference: "yellow", decision: "green", fact: "white" }[k] || "white";
}

async function fetchMemories() {
  loading.value = true;
  errMsg.value = "";
  try {
    memories.value = await listMemories({ user_id: user_id.value || "default", q: q.value, limit: 200 });
  } catch (e) {
    errMsg.value = e.message || "加载记忆失败";
    memories.value = [];
  } finally {
    loading.value = false;
  }
}

async function doAdd() {
  if (!newContent.value.trim()) return;
  try {
    await createMemory({
      user_id: user_id.value || "default",
      content: newContent.value.trim(),
      kind: newKind.value,
      tags: newTags.value.trim() || undefined,
    });
    showAdd.value = false;
    newContent.value = "";
    newTags.value = "";
    await fetchMemories();
  } catch (e) {
    errMsg.value = e.message || "写入失败";
  }
}

function askDelete(id) {
  confirmId.value = id;
}
async function doDelete() {
  if (!confirmId.value) return;
  try {
    await deleteMemory(confirmId.value, user_id.value || "default");
    confirmId.value = null;
    await fetchMemories();
  } catch (e) {
    errMsg.value = e.message || "删除失败（可能需管理员权限）";
    confirmId.value = null;
  }
}

function fmtTime(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleString("zh-CN", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
}

onMounted(fetchMemories);
</script>

<template>
  <div class="page">
    <div class="page__head">
      <h2 class="c-section-title">跨会话记忆</h2>
      <div class="row gap-2 grow">
        <CInput v-model="q" placeholder="搜索记忆内容" @keydown.enter="fetchMemories" />
        <CButton type="white" @click="fetchMemories">搜索</CButton>
        <CButton type="green" @click="showAdd = true">写入记忆</CButton>
      </div>
    </div>

    <CLoading v-if="loading" text="加载记忆…" />
    <div v-else-if="errMsg && !memories.length" class="c-card page__err">
      <CTag type="red">出错</CTag>
      <span class="comic-text">{{ errMsg }}</span>
    </div>
    <CEmpty v-else-if="!memories.length" title="还没有记忆" desc="对话中 Yue 会自动记住偏好与决策，也可以手动写入。" />

    <div v-else class="memory-grid">
      <CCard v-for="m in memories" :key="m.id" class="memory-card">
        <div class="row gap-2">
          <CTag :type="kindType(m.kind)">{{ kindLabel(m.kind) }}</CTag>
          <span class="comic-muted memory-time">{{ fmtTime(m.created_at) }}</span>
          <span class="spacer"></span>
          <button class="memory-del" @click="askDelete(m.id)" title="删除记忆">删除</button>
        </div>
        <p class="comic-text memory-content">{{ m.content }}</p>
        <div v-if="m.tags" class="row gap-1 wrap">
          <CTag v-for="t in m.tags.split(',').filter(Boolean)" :key="t" type="white">#{{ t.trim() }}</CTag>
        </div>
      </CCard>
    </div>

    <!-- 写入 -->
    <CModal :model-value="showAdd" @update:model-value="(v) => (showAdd = v)" title="写入记忆">
      <div class="stack gap-2">
        <CTextarea v-model="newContent" placeholder="记忆内容，最长 2000 字符" :rows="4" />
        <div class="row gap-2 wrap">
          <span class="comic-muted">类型:</span>
          <CButton
            v-for="k in KINDS"
            :key="k.value"
            size="sm"
            :type="newKind === k.value ? 'blue' : 'ghost'"
            @click="newKind = k.value"
          >{{ k.label }}</CButton>
        </div>
        <CInput v-model="newTags" placeholder="标签（逗号分隔，可选）" />
        <p class="comic-muted note">不要写入密码、密钥、令牌或他人的私人数据。</p>
      </div>
      <template #footer>
        <CButton type="ghost" @click="showAdd = false">取消</CButton>
        <CButton type="green" @click="doAdd">保存</CButton>
      </template>
    </CModal>

    <!-- 删除确认 -->
    <CModal :model-value="!!confirmId" @update:model-value="(v) => v || (confirmId = null)" title="删除记忆?">
      <p class="comic-text">确定删除这条记忆？</p>
      <template #footer>
        <CButton type="ghost" @click="confirmId = null">取消</CButton>
        <CButton type="red" @click="doDelete">确认删除</CButton>
      </template>
    </CModal>
  </div>
</template>

<style scoped>
.page { padding: 18px; display: flex; flex-direction: column; gap: 16px; height: 100%; overflow-y: auto; }
.page__head { display: flex; flex-direction: column; gap: 10px; }
.page__head .c-input { max-width: 420px; }
.page__err { padding: 14px; display: flex; gap: 10px; align-items: center; }
.memory-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.memory-card { padding: 14px; }
.memory-time { font-size: 12px; }
.memory-content { margin: 10px 0; white-space: pre-wrap; word-break: break-word; }
.memory-del {
  border: 2px solid var(--ink);
  background: #fff;
  font-weight: 700;
  font-size: 12px;
  padding: 2px 8px;
  cursor: pointer;
}
.memory-del:hover { background: var(--red); color: #fff; transform: scale(1.05) rotate(-2deg); }
.note { font-size: 12px; margin: 0; }
</style>
