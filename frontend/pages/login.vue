<template>
  <div class="min-h-screen flex items-center justify-center">
    <div class="text-center">
      <Icon name="ph:circle-notch" class="animate-spin w-8 h-8 text-rose-gold mx-auto mb-4" />
      <p class="text-gray-600">Redirecting to login...</p>
    </div>
  </div>
</template>

<script setup>
// Redirect to the correct auth login page
await navigateTo('/auth/login')
</script> 