import { ref, watch } from 'vue';
import { usePreferredColorScheme } from '@vueuse/core';

export function useTheme() {
  // Get system preference
  const systemPreference = usePreferredColorScheme();
  
  // Create a ref to store the current theme
  const theme = ref(null);
  
  // Function to initialize theme
  const initTheme = () => {
    // Check if theme is stored in localStorage
    const storedTheme = localStorage.getItem('nakhrali-theme');
    
    if (storedTheme) {
      // Use stored preference
      theme.value = storedTheme;
    } else {
      // Use system preference or default to light
      theme.value = systemPreference.value || 'light';
    }
    
    // Apply theme to document
    applyTheme(theme.value);
  };
  
  // Function to toggle between light and dark
  const toggleTheme = () => {
    theme.value = theme.value === 'light' ? 'dark' : 'light';
    localStorage.setItem('nakhrali-theme', theme.value);
  };
  
  // Function to set a specific theme
  const setTheme = (newTheme) => {
    if (newTheme === 'light' || newTheme === 'dark' || newTheme === 'system') {
      if (newTheme === 'system') {
        // Use system preference
        theme.value = systemPreference.value || 'light';
        localStorage.removeItem('nakhrali-theme'); // Remove stored preference
      } else {
        theme.value = newTheme;
        localStorage.setItem('nakhrali-theme', newTheme);
      }
    }
  };
  
  // Function to apply theme to document
  const applyTheme = (currentTheme) => {
    if (currentTheme === 'dark') {
      document.documentElement.classList.add('dark');
      document.body.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
      document.body.classList.remove('dark');
    }
  };
  
  // Watch for changes to theme and apply them
  watch(theme, (newTheme) => {
    applyTheme(newTheme);
  });
  
  // Watch for changes to system preference when using system theme
  watch(systemPreference, (newPreference) => {
    if (!localStorage.getItem('nakhrali-theme')) {
      // Only update if using system preference
      theme.value = newPreference;
    }
  });
  
  return {
    theme,
    initTheme,
    toggleTheme,
    setTheme,
    systemPreference
  };
}