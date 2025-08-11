<template>
  <div id="app" class="min-h-screen bg-ivory dark:bg-gray-900 transition-colors duration-300">
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
    
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg p-6 flex flex-col items-center">
        <div class="spinner w-8 h-8 mb-4"></div>
        <p class="text-gray-600 dark:text-gray-300">Loading...</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import 'vue-toastification/dist/index.css'

// Global loading state
const isLoading = ref(false)

// Provide loading state to components
provide('isLoading', isLoading)

// Set loading state
const setLoading = (loading) => {
  isLoading.value = loading
}

provide('setLoading', setLoading)

// Handle route changes
const router = useRouter()
const route = useRoute()

watch(() => route.path, () => {
  // Scroll to top on route change
  window.scrollTo(0, 0)
})

// Initialize app
onMounted(() => {
  // Check for PWA install prompt
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
      .then(registration => {
        console.log('SW registered: ', registration)
      })
      .catch(registrationError => {
        console.log('SW registration failed: ', registrationError)
      })
  }
})
</script>

<style>
/* Global styles */
html {
  scroll-behavior: smooth;
}

body {
  font-family: 'Poppins', sans-serif;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #B76E79;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #8B2635;
}

/* Focus styles for accessibility */
*:focus {
  outline: 2px solid #B76E79;
  outline-offset: 2px;
}

/* Print styles */
@media print {
  .no-print {
    display: none !important;
  }
}
</style>