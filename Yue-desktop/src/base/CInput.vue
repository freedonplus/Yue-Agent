<script setup>
defineProps({
  modelValue: { type: String, default: "" },
  type: { type: String, default: "text" },
  placeholder: { type: String, default: "" },
  dark: { type: Boolean, default: false },
});
defineEmits(["update:modelValue"]);
</script>

<template>
  <input
    class="c-input"
    :class="{ 'c-input--dark': dark }"
    :type="type"
    :placeholder="placeholder"
    :value="modelValue"
    @input="$emit('update:modelValue', $event.target.value)"
  />
</template>
