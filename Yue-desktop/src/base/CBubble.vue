<script setup>
defineProps({
  side: { type: String, default: "bot" }, // user | bot
});
</script>

<template>
  <div class="c-bubble" :class="side === 'user' ? 'c-bubble--user' : 'c-bubble--bot'">
    <slot />
  </div>
</template>
