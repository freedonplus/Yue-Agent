<script setup>
// 自定义标题栏：隐藏系统装饰后由本组件接管 拖拽 / 最小化 / 最大化 / 关闭
import { ref } from "vue";
import { getCurrentWindow } from "@tauri-apps/api/window";
import yueIcon from "../assets/yue-icon.svg";

const isTauri = typeof window !== "undefined" && "__TAURI_INTERNALS__" in window;
const win = isTauri ? getCurrentWindow() : null;
const maximized = ref(false);

if (win) {
  win.isMaximized().then((m) => (maximized.value = m));
  win.onResized(() => {
    win.isMaximized().then((m) => (maximized.value = m));
  });
}

async function minimize() {
  if (win) await win.minimize();
}
async function toggleMax() {
  if (win) await win.toggleMaximize();
}
async function close() {
  if (win) await win.close();
}
</script>

<template>
  <div class="titlebar" data-tauri-drag-region>
    <div class="titlebar__info" data-tauri-drag-region>
      <span class="titlebar__mark" data-tauri-drag-region>
        <img :src="yueIcon" alt="" class="titlebar__mark-img" aria-hidden="true" />
      </span>
      <span class="titlebar__text" data-tauri-drag-region>YUE AGENT</span>
    </div>
    <div class="titlebar__controls" data-tauri-drag-region>
      <button class="titlebar__btn" @click="minimize" aria-label="最小化" title="最小化">
        <svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true">
          <rect x="0.5" y="4.5" width="9" height="1" fill="currentColor" />
        </svg>
      </button>
      <button class="titlebar__btn" @click="toggleMax" :aria-label="maximized ? '还原' : '最大化'" :title="maximized ? '还原' : '最大化'">
        <svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true">
          <rect x="0.5" y="0.5" width="9" height="9" fill="none" stroke="currentColor" stroke-width="1.2" />
        </svg>
      </button>
      <button class="titlebar__btn titlebar__btn--close" @click="close" aria-label="关闭" title="关闭">
        <svg width="10" height="10" viewBox="0 0 10 10" aria-hidden="true">
          <path d="M0.5 0.5 L9.5 9.5 M9.5 0.5 L0.5 9.5" stroke="currentColor" stroke-width="1.4" />
        </svg>
      </button>
    </div>
  </div>
</template>

<style scoped>
.titlebar {
  height: 38px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 6px 0 12px;
  background: var(--ink);
  color: #fff;
  user-select: none;
  -webkit-user-select: none;
  border-bottom: 3px solid var(--yellow);
  position: relative;
  z-index: 10;
}
/* 半调网点微纹理 */
.titlebar::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
  background-size: 9px 9px;
}
.titlebar__info { display: flex; align-items: center; gap: 9px; }
.titlebar__mark {
  background: var(--yellow);
  color: var(--ink);
  border: 2px solid #fff;
  font-weight: 900;
  font-size: 13px;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  transform: rotate(-6deg);
  line-height: 1;
  overflow: hidden;
  flex-shrink: 0;
}
.titlebar__mark-img {
  width: 20px;
  height: 20px;
  object-fit: contain;
  display: block;
}
.titlebar__text {
  font-size: 11px;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: #fff;
  text-transform: uppercase;
}
.titlebar__controls { display: flex; gap: 5px; }
.titlebar__btn {
  width: 34px;
  height: 26px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: transparent;
  color: #ddd;
  cursor: pointer;
  border: 2px solid transparent;
  transition: transform 0.1s, background-color 0.1s, color 0.1s, border-color 0.1s, box-shadow 0.1s;
}
.titlebar__btn:hover {
  background: var(--yellow);
  color: var(--ink);
  border-color: #fff;
  transform: scale(1.12) rotate(-4deg);
  box-shadow: 2px 2px 0 0 rgba(255, 255, 255, 0.6);
}
.titlebar__btn:active {
  transform: translate(2px, 2px);
  box-shadow: none;
}
.titlebar__btn--close:hover {
  background: var(--red);
  color: #fff;
  border-color: #fff;
}
</style>
