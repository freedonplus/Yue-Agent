<script setup>
import { ref, onMounted, watch } from "vue";
import { useRouter } from "vue-router";
import { useHealth } from "./composables/useHealth";
import { useChat } from "./composables/useChat";
import { listSessions } from "./api/resources";
import CButton from "./base/CButton.vue";
import CTitleBar from "./base/CTitleBar.vue";
import yueIcon from "./assets/yue-icon.svg";

const router = useRouter();
const { online } = useHealth();
const { running, currentSessionId, loadSession, reset } = useChat();

const sessions = ref([]);
const loadingSessions = ref(false);

async function fetchSessions() {
  loadingSessions.value = true;
  try {
    sessions.value = await listSessions({ limit: 200 });
  } catch {
    sessions.value = [];
  } finally {
    loadingSessions.value = false;
  }
}

function openSession(sid) {
  if (running.value) return;
  loadSession(sid);
  router.push("/chat");
}

async function createNew() {
  reset();
  router.push("/chat");
  await fetchSessions();
}

// 会话变化后刷新列表（新建会话/发送消息后自动出现）
watch(currentSessionId, () => fetchSessions());

const navItems = [
  { path: "/models", label: "模型" },
  { path: "/memories", label: "记忆" },
  { path: "/agents", label: "档案" },
  { path: "/settings", label: "设置" },
];

function fmtTime(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  const now = Date.now();
  if (now - d.getTime() < 86400000) {
    return d.toLocaleTimeString("zh-CN", { hour: "2-digit", minute: "2-digit" });
  }
  return d.toLocaleDateString("zh-CN", { month: "2-digit", day: "2-digit" });
}

onMounted(fetchSessions);
</script>

<template>
  <div class="layout">
    <!-- 自定义标题栏（窗口控制） -->
    <CTitleBar />

    <div class="layout__body">
      <!-- 左侧：会话栏（Codex 风格） -->
      <aside class="side">
      <div class="side__top row gap-2">
        <span class="side__mark">
          <img :src="yueIcon" alt="Yue" class="side__mark-img" />
        </span>
        <div class="grow">
          <div class="comic-title side__title">YUE AGENT</div>
          <div class="row gap-1 side__status">
            <span class="c-dot" :class="online === true ? 'c-dot--online' : 'c-dot--offline'"></span>
            <span class="comic-muted side__status-text">
              {{ online === null ? "检测中" : online === true ? "在线" : "离线" }}
            </span>
          </div>
        </div>
      </div>

      <div class="side__new">
        <CButton type="red" block @click="createNew">+ 新对话</CButton>
      </div>

      <div class="side__list">
        <button
          v-for="s in sessions"
          :key="s.id"
          class="side__item"
          :class="{ 'side__item--active': s.session_id === currentSessionId }"
          @click="openSession(s.session_id)"
        >
          <div class="side__item-title text-ellipsis">{{ s.title || "未命名会话" }}</div>
          <div class="side__item-meta text-ellipsis">
            {{ s.last_message || "（空）" }}
          </div>
          <div class="side__item-time">{{ fmtTime(s.updated_at || s.created_at) }}</div>
        </button>
        <div v-if="!loadingSessions && !sessions.length" class="side__empty comic-muted">
          还没有会话，点击上方「新对话」开始
        </div>
      </div>

      <nav class="side__nav" aria-label="次级导航">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="side__nav-item"
          :class="{ 'side__nav-item--active': $route.path.startsWith(item.path) }"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>

    <!-- 右侧：主内容区 -->
    <main class="main">
      <RouterView />
    </main>
    </div>
  </div>
</template>

<style scoped>
.layout { display: flex; flex-direction: column; height: 100%; }
.layout__body { display: flex; flex: 1; min-height: 0; }
.main { flex: 1; min-width: 0; overflow: hidden; }

.side {
  width: 280px;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  background: var(--paper);
  border-right: 4px solid var(--ink);
  min-height: 0;
}
.side__top {
  padding: 14px 14px 10px;
  border-bottom: 3px solid var(--ink);
}
.side__mark {
  background: var(--yellow);
  color: #fff;
  border: 3px solid var(--ink);
  font-weight: 900;
  width: 34px;
  height: 34px;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: rotate(-6deg);
  flex-shrink: 0;
  overflow: hidden;
}
.side__mark-img { width: 26px; height: 26px; object-fit: contain; display: block; }
.side__title { font-size: 15px; letter-spacing: 0.06em; }
.side__status-text { font-size: 11px; }
.side__new { padding: 12px 14px; }
.side__list {
  flex: 1;
  overflow-y: auto;
  padding: 4px 10px 10px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-height: 0;
}
.side__item {
  text-align: left;
  border: 3px solid var(--ink);
  background: #fff;
  padding: 10px 12px;
  cursor: pointer;
  box-shadow: 3px 3px 0 0 var(--ink);
  transition: transform 0.1s, box-shadow 0.1s, background-color 0.1s;
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.side__item:hover { transform: translate(-1px, -1px); box-shadow: 4px 4px 0 0 var(--ink); background: var(--yellow); }
.side__item:active { transform: translate(3px, 3px); box-shadow: none; }
.side__item--active { background: var(--yellow); }
.side__item-title { font-weight: 900; font-size: 13px; }
.side__item-meta { font-size: 11px; color: var(--muted); font-weight: 700; }
.side__item-time { font-size: 10px; color: var(--muted); font-weight: 700; }
.side__empty { padding: 16px 6px; font-size: 12px; text-align: center; }
.side__nav {
  border-top: 3px solid var(--ink);
  display: flex;
  padding: 10px 14px;
  gap: 8px;
  flex-wrap: wrap;
}
.side__nav-item {
  flex: 1;
  text-align: center;
  padding: 7px 4px;
  border: 3px solid var(--ink);
  background: #fff;
  color: var(--ink);
  text-decoration: none;
  font-weight: 900;
  font-size: 12px;
  box-shadow: 2px 2px 0 0 var(--ink);
  transition: transform 0.1s, background-color 0.1s;
}
.side__nav-item:hover { background: var(--yellow); transform: scale(1.04); }
.side__nav-item:active { transform: translate(2px, 2px); box-shadow: none; }
.side__nav-item--active { background: var(--yellow); }

@media (max-width: 720px) {
  .side { width: 220px; }
}
</style>
