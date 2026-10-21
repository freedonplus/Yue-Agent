// 后端连通性探测
import { ref, onMounted, onBeforeUnmount } from "vue";

const online = ref(null); // null=未知, true=在线, false=离线

// 根路由与文档页不带 /api 前缀：从 BASE 推导根地址
const BASE = import.meta.env.VITE_API_BASE || "/api";
const ROOT = BASE.endsWith("/api") ? BASE.slice(0, -4) : BASE;

async function check() {
  try {
    const res = await fetch(`${ROOT}/docs/info`, { method: "GET" });
    online.value = res.ok;
  } catch {
    online.value = false;
  }
}

export function useHealth() {
  let timer = null;
  onMounted(() => {
    check();
    timer = setInterval(check, 15000);
  });
  onBeforeUnmount(() => clearInterval(timer));
  return { online, check };
}
