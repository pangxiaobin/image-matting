<template>
    <div v-if="visible" class="toast toast-center toast-middle" @click="close">
      <div :class="['alert', `alert-${type}`]">
        <span>{{ content }}</span>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  
  const props = defineProps({
    content: {
      type: String,
      required: true,
    },
    type: {
      type: String,
      default: 'info',
    },
    duration: {
      type: Number,
      default: 3000,
    },
  });
  
  const visible = ref(true);
  
  const close = () => {
    visible.value = false;
  };
  
  setTimeout(() => {
    close();
  }, props.duration);
  </script>
  <style scoped>
 .toast {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 9999;
  cursor: pointer;
  display: flex;
}
  </style>
  