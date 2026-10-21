<script setup>
import { ref } from "vue";
import { useChat } from "../composables/useChat";
import { hasAuthConfigured } from "../api/auth";
import { BASE } from "../api/http";
import CButton from "../base/CButton.vue";
import CCard from "../base/CCard.vue";
import CInput from "../base/CInput.vue";
import CTag from "../base/CTag.vue";

const { workdir, user_id, skillSlug } = useChat();

const apiBase = ref(BASE);
const authConfigured = ref(hasAuthConfigured());
const saved = ref(false);

function save() {
  // 运行时修改 workdir / user_id 立即生效（内存态）
  saved.value = true;
  setTimeout(() => (saved.value = false), 1600);
}
</script>

<template>
  <div class="page">
    <h2 class="c-section-title">设置</h2>

    <CCard class="set-card">
      <div class="comic-title set-title">连接</div>
      <div class="row gap-2">
        <CTag :type="authConfigured ? 'green' : 'white'">
          Bearer Token: {{ authConfigured ? "已配置" : "未配置（后端鉴权未开时无需）" }}
        </CTag>
      </div>
      <p class="comic-muted set-desc">
        API 地址：<code>{{ apiBase }}</code>（由 VITE_API_BASE 决定，dev 走 vite 代理）
      </p>
      <p class="comic-muted set-desc">
        AUTH_TOKEN 需与后端 .env 保持一致，配置于 .env.development / .env.production 的 VITE_AUTH_TOKEN。
      </p>
    </CCard>

    <CCard class="set-card">
      <div class="comic-title set-title">对话默认值</div>
      <div class="stack gap-3">
        <div>
          <label class="comic-muted set-label">工作目录 workdir</label>
          <CInput v-model="workdir" placeholder="例如 C:/Users/tzy88/Desktop/Yue Agent" />
        </div>
        <div>
          <label class="comic-muted set-label">记忆归属 user_id</label>
          <CInput v-model="user_id" placeholder="default" />
        </div>
        <div>
          <label class="comic-muted set-label">默认技能 skill_slug（可留空自动判断）</label>
          <CInput v-model="skillSlug" placeholder="例如 copywriting" />
        </div>
        <div class="row">
          <CButton type="green" @click="save">保存</CButton>
          <CTag v-if="saved" type="green">已保存</CTag>
        </div>
      </div>
    </CCard>

    <CCard class="set-card">
      <div class="comic-title set-title">关于</div>
      <p class="comic-text set-about">Yue Agent 桌面端</p>
      <p class="comic-muted set-desc">
        后端为本地 FastAPI 服务（LangGraph 多智能体编排），
        对话经 SSE 流式输出，敏感写操作需要人工审批。
      </p>
    </CCard>
  </div>
</template>

<style scoped>
.page { padding: 18px; display: flex; flex-direction: column; gap: 16px; height: 100%; overflow-y: auto; max-width: 640px; }
.set-card { padding: 18px; display: flex; flex-direction: column; gap: 12px; }
.set-title { font-size: 15px; }
.set-desc { margin: 0; font-size: 13px; }
.set-label { display: block; margin-bottom: 6px; font-size: 13px; }
.set-about { margin: 0; }
</style>
