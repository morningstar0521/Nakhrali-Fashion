<template>
  <div class="flex items-center">
    <button 
      @click="toggleTheme" 
      class="relative inline-flex items-center justify-center p-2 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-all duration-300 hover:scale-105"
      :class="{
        'bg-gray-100 hover:bg-gray-200 dark:bg-gray-700 dark:hover:bg-gray-600': true
      }"
      aria-label="Toggle dark mode"
    >
      <Icon v-if="theme === 'dark'" name="ph:sun-fill" class="h-5 w-5 text-yellow-400" />
      <Icon v-else name="ph:moon-fill" class="h-5 w-5 text-gray-700 dark:text-gray-200" />
    </button>
    
    <div class="ml-2 text-sm hidden md:block">
      <span class="text-gray-700 dark:text-gray-200 font-medium">{{ theme === 'dark' ? 'Light' : 'Dark' }}</span>
    </div>
  </div>
</template>

<script setup>
import { useTheme } from '~/composables/useTheme';
import { onMounted } from 'vue';

const { theme, toggleTheme, initTheme } = useTheme();

onMounted(() => {
  initTheme();
});
</script>