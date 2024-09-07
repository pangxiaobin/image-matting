<template>
    <div class="mb-4 relative">
      <div
        @click="toggleDropdown"
        class="select select-bordered w-full flex items-center justify-between cursor-pointe"
      >
        <div class="flex flex-wrap gap-1 darl:bg-gray-700">
          <span v-for="item in modelValue" :key="item" class="px-2 bg-blue-100 text-blue-800 py-1 rounded text-sm ml-2">
            {{ item }}
            <button @click.stop="removeItem(item)" class="ml-1 text-blue-600 hover:text-blue-800">&times;</button>
          </span>
        </div>
      </div>
      <div v-if="isOpen" class="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg">
        <div
          v-for="option in options"
          :key="option"
          @click="toggleOption(option)"
          class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
        >
          <input type="checkbox" :checked="modelValue.includes(option)" class="mr-2">
          {{ option }}
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, defineProps, defineEmits } from 'vue';
  
  const props = defineProps({
    modelValue: {
      type: Array,
      required: true
    },
    options: {
      type: Array,
      required: true
    }
  });
  
  const emit = defineEmits(['update:modelValue']);
  
  const isOpen = ref(false);
  
  const toggleDropdown = () => {
    isOpen.value = !isOpen.value;
  };
  
  const toggleOption = (option) => {
    const newValue = [...props.modelValue];
    const index = newValue.indexOf(option);
    if (index === -1) {
      newValue.push(option);
    } else {
      newValue.splice(index, 1);
    }
    emit('update:modelValue', newValue);
  };
  
  const removeItem = (item) => {
    const newValue = props.modelValue.filter(i => i !== item);
    emit('update:modelValue', newValue);
  };
  </script>