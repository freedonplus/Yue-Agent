// ============================================================
// 资源接口：厂商 / 员工 / 工具 / 技能 / 会话 / 记忆
// ============================================================
import { request } from "./http";

/* ---------- 厂商 Provider ---------- */
export const listProviders = (q) => request("/providers", { params: { q } });
export const getProvider = (id) => request(`/providers/${id}`);
export const createProvider = (body) => request("/providers", { method: "POST", body });
export const updateProvider = (id, body) => request(`/providers/${id}`, { method: "PATCH", body });
export const setProviderEnabled = (id, enabled) =>
  request(`/providers/${id}/enabled`, { method: "PATCH", body: { enabled } });

/* ---------- 员工 AgentRole ---------- */
export const listAgentRoles = (params) => request("/agent_roles", { params });
export const getAgentRole = (id) => request(`/agent_roles/${id}`);
export const setAgentEnabled = (id, enabled) =>
  request(`/agent_roles/${id}/enabled`, { method: "PATCH", body: { enabled } });
export const getAgentTools = (id) => request(`/agent_roles/${id}/tools`);
export const putAgentTools = (id, tools) =>
  request(`/agent_roles/${id}/tools`, { method: "PUT", body: { tools } });

/* ---------- 工具 Tool ---------- */
export const listTools = () => request("/tools");
export const getTool = (id) => request(`/tools/${id}`);
export const createTool = (body) => request("/tools", { method: "POST", body });
export const updateTool = (id, body) => request(`/tools/${id}`, { method: "PATCH", body });
export const setToolEnabled = (id, enabled) =>
  request(`/tools/${id}/enabled`, { method: "PATCH", body: { enabled } });
export const refreshTool = (id) => request(`/tools/${id}/refresh`, { method: "POST" });

/* ---------- 技能 Skill ---------- */
export const listSkills = () => request("/skills");
export const listSkillSummary = () => request("/skills/summary");
export const getSkill = (id) => request(`/skills/${id}`);

/* ---------- 会话 Session ---------- */
export const listSessions = (params) => request("/sessions", { params });
export const createSession = (body) => request("/sessions", { method: "POST", body });
export const getSession = (id) => request(`/sessions/${id}`);
export const getSessionMessages = (id, params) => request(`/sessions/${id}/messages`, { params });
export const updateSession = (id, body) => request(`/sessions/${id}`, { method: "PATCH", body });
export const deleteSession = (id) => request(`/sessions/${id}`, { method: "DELETE" });

/* ---------- 记忆 Memory ---------- */
export const listMemories = (params) => request("/memories", { params });
export const createMemory = (body) => request("/memories", { method: "POST", body });
export const deleteMemory = (id, user_id) =>
  request(`/memories/${id}`, { method: "DELETE", params: { user_id } });
