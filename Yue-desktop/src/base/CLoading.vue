<script setup>
defineProps({
  text: { type: String, default: "加载中…" },
});
</script>

<template>
  <div class="c-loading row gap-2" role="status">
    <span class="c-dot c-dot--online"></span>
    <span>{{ text }}</span>
  </div>
</template>
