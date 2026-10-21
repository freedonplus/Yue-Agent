<script setup>
defineProps({
  paper: { type: Boolean, default: false },
});
</script>

<template>
  <div class="c-card" :class="{ 'c-card--paper': paper }">
    <slot />
  </div>
</template>
