<script setup>
defineProps({
  type: { type: String, default: "" }, // red | blue | green | white | dark | ghost
  size: { type: String, default: "" }, // sm | lg
  block: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
});
</script>

<template>
  <button
    class="c-btn"
    :class="[
      type ? `c-btn--${type}` : '',
      size ? `c-btn--${size}` : '',
      block ? 'c-btn--block' : '',
    ]"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>
