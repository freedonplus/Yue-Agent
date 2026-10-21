<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from "vue";

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  title: { type: String, default: "" },
  width: { type: String, default: "520px" },
});
const emit = defineEmits(["update:modelValue", "close"]);
const show = ref(props.modelValue);

watch(
  () => props.modelValue,
  (v) => {
    show.value = v;
    if (v) document.addEventListener("keydown", onKey);
    else document.removeEventListener("keydown", onKey);
  }
);
function close() {
  show.value = false;
  emit("update:modelValue", false);
  emit("close");
}
function onKey(e) {
  if (e.key === "Escape") close();
}
onMounted(() => {
  if (show.value) document.addEventListener("keydown", onKey);
});
onBeforeUnmount(() => document.removeEventListener("keydown", onKey));
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="show" class="c-modal" @click.self="close" role="dialog" aria-modal="true">
        <div class="c-modal__box" :style="{ maxWidth: width }">
          <div class="c-modal__head">
            <span class="c-modal__title comic-title">{{ title }}</span>
            <button class="c-modal__x" @click="close" aria-label="关闭">✕</button>
          </div>
          <div class="c-modal__body">
            <slot />
          </div>
          <div v-if="$slots.footer" class="c-modal__foot">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.c-modal {
  position: fixed;
  inset: 0;
  z-index: 100;
  background: rgba(26, 26, 26, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}
.c-modal__box {
  width: 100%;
  background: var(--paper);
  border: 4px solid var(--ink);
  box-shadow: 8px 8px 0 0 var(--ink);
  position: relative;
}
.c-modal__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 4px solid var(--ink);
  background: var(--yellow);
}
.c-modal__title { font-size: 16px; }
.c-modal__x {
  border: 3px solid var(--ink);
  background: #fff;
  width: 30px;
  height: 30px;
  font-weight: 900;
  cursor: pointer;
  transition: transform 0.1s, box-shadow 0.1s;
}
.c-modal__x:hover { transform: scale(1.15) rotate(8deg); box-shadow: 3px 3px 0 0 var(--ink); }
.c-modal__x:active { transform: translate(2px, 2px); box-shadow: none; }
.c-modal__body { padding: 18px 16px; max-height: 70vh; overflow-y: auto; }
.c-modal__foot {
  padding: 12px 16px;
  border-top: 3px solid var(--ink);
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
.modal-enter-active, .modal-leave-active { transition: opacity 0.12s; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
</style>
