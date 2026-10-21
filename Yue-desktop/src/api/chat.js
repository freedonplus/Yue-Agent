// ============================================================
// 对话接口（SSE 流式）
// 浏览器 EventSource 不支持 POST，必须 fetch + ReadableStream 手解 SSE。
// 提供流式迭代器：每行 data: {...} 解析为一个事件对象。
// ============================================================
import { getToken } from "./auth";

const BASE = import.meta.env.VITE_API_BASE || "/api";

async function openStream(path, body) {
  const token = await getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${BASE}${path}`, {
    method: "POST",
    headers,
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    const err = new Error(data.message || `请求失败 (${res.status})`);
    err.status = res.status;
    err.code = data.code || "HTTP_ERROR";
    throw err;
  }
  if (!res.body) throw new Error("服务端不支持流式响应");
  return res.body.getReader();
}

// 读取一个流，回调每个事件；返回 Promise。
export function consumeStream(path, payload, onEvent, { signal } = {}) {
  return openStream(path, payload).then(async (reader) => {
    const decoder = new TextDecoder();
    let buf = "";
    try {
      for (;;) {
        if (signal && signal.aborted) {
          await reader.cancel();
          break;
        }
        const { done, value } = await reader.read();
        if (done) break;
        buf += decoder.decode(value, { stream: true });
        let idx;
        while ((idx = buf.indexOf("\n")) >= 0) {
          const line = buf.slice(0, idx).trim();
          buf = buf.slice(idx + 1);
          if (!line) continue;
          if (!line.startsWith("data:")) continue;
          const raw = line.slice(5).trim();
          if (!raw) continue;
          let evt;
          try {
            evt = JSON.parse(raw);
          } catch {
            continue; // 非 JSON 行忽略
          }
          onEvent(evt);
        }
      }
      // 结尾残余
      const rest = buf.trim();
      if (rest.startsWith("data:")) {
        const raw = rest.slice(5).trim();
        if (raw) {
          try {
            onEvent(JSON.parse(raw));
          } catch { /* ignore */ }
        }
      }
    } finally {
      reader.releaseLock();
    }
  });
}
