import { useTheme } from '~/composables/useTheme';

export default defineNuxtPlugin(nuxtApp => {
  // Initialize theme when app is mounted
  nuxtApp.hook('app:mounted', () => {
    const { initTheme } = useTheme();
    initTheme();
  });
});