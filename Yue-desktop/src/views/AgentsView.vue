<script setup>
import { ref, onMounted, computed } from "vue";
import {
  listAgentRoles,
  listTools,
  listSkillSummary,
  listProviders,
  getAgentTools,
  setAgentEnabled,
} from "../api/resources";
import CButton from "../base/CButton.vue";
import CCard from "../base/CCard.vue";
import CTag from "../base/CTag.vue";
import CEmpty from "../base/CEmpty.vue";
import CLoading from "../base/CLoading.vue";
import CModal from "../base/CModal.vue";

const tab = ref("roles"); // roles | tools | skills | providers
const loading = ref(false);
const errMsg = ref("");
const roles = ref([]);
const tools = ref([]);
const skills = ref([]);
const providers = ref([]);
const detail = ref(null); // 员工详情弹窗
const detailTools = ref([]);

async function load() {
  loading.value = true;
  errMsg.value = "";
  try {
    const [r, t, s, p] = await Promise.all([
      // 管理端需要看到停用员工，否则停用后无法再启用
      listAgentRoles({ include_disabled: true }).catch(() => []),
      listTools().catch(() => []),
      listSkillSummary().catch(() => []),
      listProviders("").catch(() => []),
    ]);
    roles.value = r;
    tools.value = t;
    skills.value = s;
    providers.value = p;
  } catch (e) {
    errMsg.value = e.message || "加载失败";
  } finally {
    loading.value = false;
  }
}

const supervisors = computed(() => roles.value.filter((r) => r.role === "supervisor"));
const workers = computed(() => roles.value.filter((r) => r.role === "worker"));

async function showRoleDetail(role) {
  detail.value = role;
  detailTools.value = [];
  try {
    detailTools.value = await getAgentTools(role.id);
  } catch {
    detailTools.value = [];
  }
}

// 员工启停
const togglingId = ref(null);
async function toggleEnabled(role) {
  if (togglingId.value) return;
  togglingId.value = role.id;
  try {
    await setAgentEnabled(role.id, !role.enabled);
    role.enabled = !role.enabled;
    await load();
  } catch (e) {
    errMsg.value = e.message || "操作失败";
  } finally {
    togglingId.value = null;
  }
}

const toolName = (tid) => tools.value.find((t) => t.id === tid)?.name || tid;

onMounted(load);
</script>

<template>
  <div class="page">
    <div class="page__head">
      <h2 class="c-section-title">智能体档案</h2>
      <div class="row gap-2 wrap">
        <CButton :type="tab === 'roles' ? 'red' : 'ghost'" @click="tab = 'roles'">员工</CButton>
        <CButton :type="tab === 'tools' ? 'blue' : 'ghost'" @click="tab = 'tools'">工具</CButton>
        <CButton :type="tab === 'skills' ? 'green' : 'ghost'" @click="tab = 'skills'">技能</CButton>
        <CButton :type="tab === 'providers' ? 'yellow' : 'ghost'" @click="tab = 'providers'">厂商</CButton>
        <span class="spacer"></span>
        <CButton type="white" size="sm" @click="load">刷新</CButton>
      </div>
    </div>

    <CLoading v-if="loading" text="加载档案…" />
    <div v-else-if="errMsg && !roles.length && !tools.length" class="c-card page__err">
      <CTag type="red">出错</CTag>
      <span class="comic-text">{{ errMsg }}</span>
    </div>

    <!-- 员工 -->
    <template v-if="tab === 'roles'">
      <section v-if="supervisors.length">
        <h3 class="comic-title section-sub">调度员</h3>
        <div class="grid">
          <CCard v-for="r in supervisors" :key="r.id" class="role-card group" @click="showRoleDetail(r)">
            <div class="row gap-2 wrap">
              <span class="comic-title">{{ r.name }}</span>
              <CTag type="red">SUPERVISOR</CTag>
              <CTag :type="r.enabled ? 'green' : 'white'">{{ r.enabled ? "启用" : "停用" }}</CTag>
              <span class="spacer"></span>
              <button
                class="role-toggle"
                :class="r.enabled ? 'role-toggle--off' : 'role-toggle--on'"
                @click.stop="toggleEnabled(r)"
                :disabled="togglingId === r.id"
              >
                {{ r.enabled ? "停用" : "启用" }}
              </button>
            </div>
            <p class="comic-muted role-desc">{{ r.description || "无描述" }}</p>
          </CCard>
        </div>
      </section>
      <section v-if="workers.length">
        <h3 class="comic-title section-sub">员工</h3>
        <div class="grid">
          <CCard v-for="r in workers" :key="r.id" class="role-card group" @click="showRoleDetail(r)">
            <div class="row gap-2 wrap">
              <span class="comic-title">{{ r.name }}</span>
              <CTag type="blue">{{ r.slug }}</CTag>
              <CTag :type="r.enabled ? 'green' : 'white'">{{ r.enabled ? "启用" : "停用" }}</CTag>
              <CTag v-if="r.is_output_gate" type="yellow">输出管卡</CTag>
              <span class="spacer"></span>
              <button
                class="role-toggle"
                :class="r.enabled ? 'role-toggle--off' : 'role-toggle--on'"
                @click.stop="toggleEnabled(r)"
                :disabled="togglingId === r.id"
              >
                {{ r.enabled ? "停用" : "启用" }}
              </button>
            </div>
            <p class="comic-muted role-desc">{{ r.description || "无描述" }}</p>
            <div class="row gap-1 wrap">
              <CTag v-for="t in r.approval_tools || []" :key="t" type="white">{{ t.split("_").slice(-1)[0] }}</CTag>
            </div>
          </CCard>
        </div>
      </section>
      <CEmpty v-if="!supervisors.length && !workers.length" title="暂无员工" desc="后端未连接或未配置员工。" />
    </template>

    <!-- 工具 -->
    <template v-if="tab === 'tools'">
      <CEmpty v-if="!tools.length" title="暂无工具" desc="后端未连接或未配置 MCP 工具。" />
      <div class="grid">
        <CCard v-for="t in tools" :key="t.id" class="role-card group">
          <div class="row gap-2 wrap">
            <span class="comic-title">{{ t.name }}</span>
            <CTag type="blue">{{ t.slug }}</CTag>
            <CTag :type="t.enabled ? 'green' : 'white'">{{ t.enabled ? "启用" : "停用" }}</CTag>
          </div>
          <p class="comic-muted role-desc">{{ t.description || "无描述" }}</p>
          <div class="row gap-1 wrap">
            <CTag v-for="s in t.servers || []" :key="s" type="white">{{ s }}</CTag>
            <CTag type="yellow" v-if="(t.available_tools || []).length">{{ (t.available_tools || []).length }} 个工具</CTag>
          </div>
        </CCard>
      </div>
    </template>

    <!-- 技能 -->
    <template v-if="tab === 'skills'">
      <CEmpty v-if="!skills.length" title="暂无技能" desc="后端未连接或未导入技能。" />
      <div class="grid">
        <CCard v-for="s in skills" :key="s.id" class="role-card group">
          <div class="row gap-2 wrap">
            <span class="comic-title">{{ s.name || s.slug }}</span>
            <CTag type="blue">{{ s.slug }}</CTag>
            <CTag :type="s.enabled ? 'green' : 'white'">{{ s.enabled ? "启用" : "停用" }}</CTag>
          </div>
          <p class="comic-muted role-desc">{{ s.description || "无描述" }}</p>
        </CCard>
      </div>
    </template>

    <!-- 厂商 -->
    <template v-if="tab === 'providers'">
      <CEmpty v-if="!providers.length" title="暂无厂商" desc="后端未连接或未配置厂商。" />
      <div class="grid">
        <CCard v-for="p in providers" :key="p.id" class="role-card group">
          <div class="row gap-2 wrap">
            <span class="comic-title">{{ p.name }}</span>
            <CTag type="blue">{{ p.slug }}</CTag>
            <CTag v-if="p.is_default" type="yellow">默认</CTag>
            <CTag :type="p.enabled ? 'green' : 'white'">{{ p.enabled ? "启用" : "停用" }}</CTag>
          </div>
          <p class="comic-muted role-desc">{{ p.base_url }}</p>
          <div class="row gap-2 wrap">
            <CTag type="white">模型: {{ p.default_model || "未设" }}</CTag>
            <CTag type="white">temp: {{ p.temperature }}</CTag>
            <CTag type="white">max: {{ p.max_tokens }}</CTag>
          </div>
        </CCard>
      </div>
    </template>

    <!-- 员工详情 -->
    <CModal :model-value="!!detail" @update:model-value="(v) => v || (detail = null)" :title="detail?.name || ''">
      <div v-if="detail" class="stack gap-3">
        <div class="row gap-2 wrap">
          <CTag type="blue">{{ detail.slug }}</CTag>
          <CTag :type="detail.role === 'supervisor' ? 'red' : 'blue'">{{ detail.role }}</CTag>
          <CTag :type="detail.enabled ? 'green' : 'white'">{{ detail.enabled ? "启用" : "停用" }}</CTag>
        </div>
        <p class="comic-text detail-desc">{{ detail.description || "无描述" }}</p>
        <div>
          <div class="comic-title section-sub">系统提示词</div>
          <pre class="detail-prompt">{{ detail.system_prompt }}</pre>
        </div>
        <div v-if="detailTools.length">
          <div class="comic-title section-sub">挂载工具</div>
          <div class="row gap-1 wrap">
            <CTag v-for="mt in detailTools" :key="mt.tool_id" type="white">
              {{ mt.name || toolName(mt.tool_id) }}
            </CTag>
          </div>
        </div>
      </div>
    </CModal>
  </div>
</template>

<style scoped>
.page { padding: 18px; display: flex; flex-direction: column; gap: 16px; height: 100%; overflow-y: auto; }
.page__head { display: flex; flex-direction: column; gap: 10px; }
.page__err { padding: 14px; display: flex; gap: 10px; align-items: center; }
.section-sub { font-size: 14px; margin: 6px 0 10px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 16px; }
.role-card { padding: 14px; cursor: pointer; display: flex; flex-direction: column; gap: 8px; }
.role-card:hover { transform: translate(-2px, -2px); box-shadow: var(--shadow-hover); }
.role-desc { margin: 0; font-size: 12px; }
.role-toggle {
  border: 2px solid var(--ink);
  font-weight: 900;
  font-size: 11px;
  padding: 3px 10px;
  cursor: pointer;
  transition: transform 0.1s;
}
.role-toggle:hover { transform: scale(1.08) rotate(-2deg); }
.role-toggle:disabled { opacity: 0.5; cursor: wait; }
.role-toggle--off { background: #fff; color: var(--ink); }
.role-toggle--off:hover { background: var(--red); color: #fff; }
.role-toggle--on { background: var(--green); color: #fff; }
.role-toggle--on:hover { background: var(--red); color: #fff; }
.detail-desc { margin: 0; }
.detail-prompt {
  background: var(--ink);
  color: var(--yellow);
  font-family: var(--mono);
  font-size: 12px;
  padding: 12px;
  white-space: pre-wrap;
  max-height: 220px;
  overflow-y: auto;
  margin-top: 6px;
}
</style>
