<script setup>
import { ref, watch } from "vue";

const props = defineProps({
  modelValue: { type: String, default: "" },
  placeholder: { type: String, default: "" },
  rows: { type: Number, default: 4 },
});
const emit = defineEmits(["update:modelValue"]);
const inner = ref(props.modelValue);
watch(() => props.modelValue, (v) => { inner.value = v; });
function onInput() { emit("update:modelValue", inner.value); }
</script>

<template>
  <textarea
    class="c-textarea"
    :placeholder="placeholder"
    :rows="rows"
    v-model="inner"
    @input="onInput"
  ></textarea>
</template>
