<script setup>
import { ref, onMounted } from "vue";
import {
  listProviders,
  createProvider,
  updateProvider,
  setProviderEnabled,
} from "../api/resources";
import CButton from "../base/CButton.vue";
import CCard from "../base/CCard.vue";
import CInput from "../base/CInput.vue";
import CTextarea from "../base/CTextarea.vue";
import CTag from "../base/CTag.vue";
import CModal from "../base/CModal.vue";
import CEmpty from "../base/CEmpty.vue";
import CLoading from "../base/CLoading.vue";

const providers = ref([]);
const loading = ref(false);
const errMsg = ref("");
const showForm = ref(false);
const editing = ref(null); // null=新建, {provider}=编辑
const saving = ref(false);

// 表单
const form = ref(emptyForm());
function emptyForm() {
  return {
    slug: "",
    name: "",
    base_url: "",
    api_key: "",
    default_model: "",
    temperature: 0.7,
    max_tokens: 4096,
    max_retries: 3,
    request_timeout: 60,
    enabled: true,
    is_default: false,
  };
}

async function load() {
  loading.value = true;
  errMsg.value = "";
  try {
    providers.value = await listProviders("");
  } catch (e) {
    errMsg.value = e.message || "加载厂商失败";
    providers.value = [];
  } finally {
    loading.value = false;
  }
}

function openNew() {
  editing.value = null;
  form.value = emptyForm();
  showForm.value = true;
}
function openEdit(p) {
  editing.value = p;
  form.value = {
    slug: p.slug,
    name: p.name,
    base_url: p.base_url,
    api_key: "", // 已掩码，留空表示不修改
    default_model: p.default_model || "",
    temperature: p.temperature ?? 0.7,
    max_tokens: p.max_tokens ?? 4096,
    max_retries: p.max_retries ?? 3,
    request_timeout: p.request_timeout ?? 60,
    enabled: p.enabled,
    is_default: p.is_default,
  };
  showForm.value = true;
}

async function save() {
  if (!form.value.slug.trim() || !form.value.name.trim() || !form.value.base_url.trim()) {
    errMsg.value = "slug、名称、地址为必填项";
    return;
  }
  saving.value = true;
  errMsg.value = "";
  try {
    const body = { ...form.value };
    if (editing.value) {
      // 编辑：api_key 留空表示保持原值
      if (!body.api_key) delete body.api_key;
      await updateProvider(editing.value.id, body);
    } else {
      if (!body.api_key) delete body.api_key;
      await createProvider(body);
    }
    showForm.value = false;
    await load();
  } catch (e) {
    errMsg.value = e.message || "保存失败";
  } finally {
    saving.value = false;
  }
}

async function toggleEnabled(p) {
  try {
    await setProviderEnabled(p.id, !p.enabled);
    p.enabled = !p.enabled;
    await load();
  } catch (e) {
    errMsg.value = e.message || "操作失败";
  }
}

function fmtTime(iso) {
  if (!iso) return "";
  return new Date(iso).toLocaleString("zh-CN", { month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit" });
}

onMounted(load);
</script>

<template>
  <div class="page">
    <div class="page__head">
      <h2 class="c-section-title">模型 / 厂商配置</h2>
      <div class="row gap-2">
        <CButton type="white" @click="load">刷新</CButton>
        <CButton type="green" @click="openNew">新增厂商</CButton>
      </div>
    </div>

    <CLoading v-if="loading" text="加载厂商…" />
    <div v-else-if="errMsg && !providers.length" class="c-card page__err">
      <CTag type="red">出错</CTag>
      <span class="comic-text">{{ errMsg }}</span>
    </div>
    <CEmpty v-else-if="!providers.length" title="暂无厂商" desc="添加一个模型厂商（如 DeepSeek / OpenAI 兼容接口）开始使用。" />

    <div v-else class="provider-list">
      <CCard v-for="p in providers" :key="p.id" class="provider-card">
        <div class="row gap-2 wrap">
          <span class="comic-title">{{ p.name }}</span>
          <CTag type="blue">{{ p.slug }}</CTag>
          <CTag v-if="p.is_default" type="yellow">默认</CTag>
          <CTag :type="p.enabled ? 'green' : 'white'">{{ p.enabled ? "启用" : "停用" }}</CTag>
          <span class="spacer"></span>
          <button class="provider-btn" @click="openEdit(p)">编辑</button>
          <button
            class="provider-btn"
            :class="p.enabled ? 'provider-btn--off' : 'provider-btn--on'"
            @click="toggleEnabled(p)"
          >
            {{ p.enabled ? "停用" : "启用" }}
          </button>
        </div>
        <div class="comic-muted provider-url">{{ p.base_url }}</div>
        <div class="row gap-2 wrap provider-meta">
          <CTag type="white">模型: {{ p.default_model || "未设" }}</CTag>
          <CTag type="white">temp: {{ p.temperature }}</CTag>
          <CTag type="white">max: {{ p.max_tokens }}</CTag>
          <CTag type="white">超时: {{ p.request_timeout }}s</CTag>
          <CTag type="white">重试: {{ p.max_retries }}</CTag>
        </div>
        <div class="comic-muted provider-time">更新于 {{ fmtTime(p.updated_at) }}</div>
      </CCard>
    </div>

    <!-- 新增 / 编辑弹窗 -->
    <CModal
      :model-value="showForm"
      @update:model-value="(v) => (showForm = v)"
      :title="editing ? '编辑厂商' : '新增厂商'"
      width="600px"
    >
      <div class="stack gap-3">
        <div class="row gap-2">
          <div class="grow">
            <label class="comic-muted form-label">slug（唯一标识）</label>
            <CInput v-model="form.slug" placeholder="deepseek" />
          </div>
          <div class="grow">
            <label class="comic-muted form-label">显示名称</label>
            <CInput v-model="form.name" placeholder="DeepSeek" />
          </div>
        </div>
        <div>
          <label class="comic-muted form-label">Base URL（http/https）</label>
          <CInput v-model="form.base_url" placeholder="https://api.deepseek.com" />
        </div>
        <div class="row gap-2">
          <div class="grow">
            <label class="comic-muted form-label">API Key（{{ editing ? "留空表示不修改" : "必填" }}）</label>
            <CInput v-model="form.api_key" type="password" placeholder="sk-..." />
          </div>
          <div class="grow">
            <label class="comic-muted form-label">默认模型</label>
            <CInput v-model="form.default_model" placeholder="deepseek-chat" />
          </div>
        </div>
        <div class="row gap-2 wrap">
          <div class="grow">
            <label class="comic-muted form-label">温度 (0-2)</label>
            <CInput v-model="form.temperature" type="number" />
          </div>
          <div class="grow">
            <label class="comic-muted form-label">max_tokens</label>
            <CInput v-model="form.max_tokens" type="number" />
          </div>
          <div class="grow">
            <label class="comic-muted form-label">max_retries</label>
            <CInput v-model="form.max_retries" type="number" />
          </div>
          <div class="grow">
            <label class="comic-muted form-label">超时(秒)</label>
            <CInput v-model="form.request_timeout" type="number" />
          </div>
        </div>
        <div class="row gap-3 wrap">
          <label class="row gap-1 comic-muted form-check">
            <input type="checkbox" v-model="form.enabled" /> 启用
          </label>
          <label class="row gap-1 comic-muted form-check">
            <input type="checkbox" v-model="form.is_default" /> 设为默认（全局唯一）
          </label>
        </div>
      </div>
      <div v-if="errMsg" class="comic-text form-err">{{ errMsg }}</div>
      <template #footer>
        <CButton type="ghost" @click="showForm = false">取消</CButton>
        <CButton type="green" @click="save" :disabled="saving">{{ saving ? "保存中…" : "保存" }}</CButton>
      </template>
    </CModal>
  </div>
</template>

<style scoped>
.page { padding: 18px; display: flex; flex-direction: column; gap: 16px; height: 100%; overflow-y: auto; }
.page__head { display: flex; justify-content: space-between; align-items: center; gap: 10px; flex-wrap: wrap; }
.page__err { padding: 14px; display: flex; gap: 10px; align-items: center; }
.provider-list { display: flex; flex-direction: column; gap: 14px; }
.provider-card { padding: 16px; display: flex; flex-direction: column; gap: 10px; }
.provider-url { font-size: 12px; word-break: break-all; }
.provider-meta { flex-wrap: wrap; }
.provider-time { font-size: 11px; }
.provider-btn {
  border: 2px solid var(--ink);
  background: #fff;
  font-weight: 900;
  font-size: 12px;
  padding: 4px 12px;
  cursor: pointer;
  transition: transform 0.1s;
}
.provider-btn:hover { transform: scale(1.06); background: var(--yellow); }
.provider-btn--off:hover { background: var(--red); color: #fff; }
.provider-btn--on { background: var(--green); color: #fff; }
.provider-btn--on:hover { background: var(--red); color: #fff; }
.form-label { display: block; margin-bottom: 5px; font-size: 12px; }
.form-check { font-size: 13px; cursor: pointer; }
.form-check input { width: 16px; height: 16px; accent-color: var(--red); }
.form-err { color: var(--red); margin-top: 8px; font-size: 13px; }
</style>
