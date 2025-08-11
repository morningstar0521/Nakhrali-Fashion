<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-ivory to-rose-gold/10">
    <div class="text-center max-w-md w-full px-4">
      <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-rose-gold/10 mb-6">
        <Icon name="ph:sign-out" class="h-8 w-8 text-rose-gold" />
      </div>
      <h1 class="text-2xl font-display font-bold text-deep-maroon mb-2">Logging Out</h1>
      <p class="text-gray-600 mb-6">Please wait while we log you out...</p>
      <div class="flex justify-center">
        <Icon name="ph:circle-notch" class="animate-spin w-8 h-8 text-rose-gold" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter();
const toast = useToast();
const { logout } = useAuth();

onMounted(async () => {
  try {
    await logout();
    toast.success('You have been successfully logged out.');
  } catch (error) {
    console.error('Logout error:', error);
    toast.error('There was an issue logging you out.');
  } finally {
    // Redirect to home page after a short delay
    setTimeout(() => {
      router.push('/');
    }, 1500);
  }
});
</script>