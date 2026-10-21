// ============================================================
// HTTP 封装
// 统一错误格式：{ code, message, detail, request_id, status }
// ============================================================
import { getToken } from "./auth";

const BASE = import.meta.env.VITE_API_BASE || "/api";

function buildUrl(path, params) {
  const url = `${BASE}${path}`;
  if (!params) return url;
  const qs = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== "") qs.set(k, v);
  });
  const s = qs.toString();
  return s ? `${url}?${s}` : url;
}

export async function request(path, { method = "GET", body, params } = {}) {
  const token = await getToken();
  const headers = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(buildUrl(path, params), {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (res.status === 204) return null;

  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    const err = new Error(data.message || `请求失败 (${res.status})`);
    err.status = res.status;
    err.code = data.code || "HTTP_ERROR";
    err.detail = data.detail ?? null;
    err.requestId = data.request_id ?? null;
    throw err;
  }
  return data;
}

export { BASE };
