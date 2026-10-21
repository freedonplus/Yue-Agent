<script setup>
defineProps({
  title: { type: String, default: "" },
  desc: { type: String, default: "" },
  icon: { type: String, default: "" },
});
</script>

<template>
  <div class="c-empty">
    <div class="c-empty__icon" aria-hidden="true">
      <img v-if="icon" :src="icon" alt="" class="c-empty__img" />
      <template v-else>?</template>
    </div>
    <div class="comic-title c-empty__title">{{ title }}</div>
    <div v-if="desc" class="comic-muted c-empty__desc">{{ desc }}</div>
    <div v-if="$slots.default" class="c-empty__action">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.c-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px 20px;
  text-align: center;
  gap: 10px;
}
.c-empty__icon {
  width: 56px;
  height: 56px;
  border: 4px solid var(--ink);
  background: var(--yellow);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 26px;
  transform: rotate(-6deg);
  box-shadow: 4px 4px 0 0 var(--ink);
  overflow: hidden;
}
.c-empty__img { width: 44px; height: 44px; object-fit: contain; display: block; }
.c-empty__title { font-size: 18px; }
.c-empty__desc { font-size: 13px; max-width: 380px; }
</style>
