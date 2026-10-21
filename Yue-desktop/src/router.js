import { createRouter, createWebHashHistory } from "vue-router";

const routes = [
  { path: "/", redirect: "/chat" },
  { path: "/chat", component: () => import("./views/ChatView.vue") },
  { path: "/sessions", component: () => import("./views/SessionsView.vue") },
  { path: "/memories", component: () => import("./views/MemoriesView.vue") },
  { path: "/agents", component: () => import("./views/AgentsView.vue") },
  { path: "/models", component: () => import("./views/ModelsView.vue") },
  { path: "/settings", component: () => import("./views/SettingsView.vue") },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes,
});
