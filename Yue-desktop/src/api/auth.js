// ============================================================
// Bearer Token 生成
// 前后端共享 .env 中的 AUTH_TOKEN（HMAC 签名密钥），
// 前端生成带过期时间的 token，后端只校验。
// 未配置 VITE_AUTH_TOKEN 时返回 null（后端鉴权未开，直接放行）。
// ============================================================

const SECRET = import.meta.env.VITE_AUTH_TOKEN || "";

let cached = null; // { token, exp }

function b64url(data) {
  // 接受 Uint8Array 或 string
  let bytes = data;
  if (typeof data === "string") {
    bytes = new TextEncoder().encode(data);
  }
  let bin = "";
  bytes.forEach((b) => (bin += String.fromCharCode(b)));
  return btoa(bin).replace(/=+$/, "").replace(/\+/g, "-").replace(/\//g, "_");
}

async function hmacSha256(secret, message) {
  const enc = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw",
    enc.encode(secret),
    { name: "HMAC", hash: "SHA-256" },
    false,
    ["sign"]
  );
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(message));
  return new Uint8Array(sig);
}

export async function getToken(ttl = 300) {
  if (!SECRET) return null;

  const now = Math.floor(Date.now() / 1000);
  // 提前 30 秒刷新，避免边缘过期
  if (cached && cached.exp - 30 > now) return cached.token;

  const payload = JSON.stringify({ iat: now, exp: now + ttl });
  const payloadPart = b64url(payload);
  const sig = await hmacSha256(SECRET, payloadPart);
  const token = `${payloadPart}.${b64url(sig)}`;
  cached = { token, exp: now + ttl };
  return token;
}

export function hasAuthConfigured() {
  return !!SECRET;
}
