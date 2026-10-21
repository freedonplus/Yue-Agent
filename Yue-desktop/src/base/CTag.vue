<script setup>
defineProps({
  type: { type: String, default: "" }, // red | blue | green | dark | white
});
</script>

<template>
  <span class="c-tag" :class="type ? `c-tag--${type}` : ''">
    <slot />
  </span>
</template>
