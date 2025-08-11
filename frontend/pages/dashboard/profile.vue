<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Page Header -->
      <div class="mb-8 text-center md:text-left">
        <h1 class="text-3xl font-display font-bold text-deep-maroon mb-2">
          My Profile
        </h1>
        <p class="text-gray-600">
          Manage your personal information and preferences
        </p>
      </div>
      
      <!-- Profile Form -->
      <div class="bg-white rounded-lg shadow-md p-6 border border-gray-100">
        <form @submit.prevent="updateProfile">
          <!-- Profile Picture -->
          <div class="flex flex-col items-center mb-8">
            <div class="relative">
              <div v-if="profilePicture" class="w-24 h-24 rounded-full overflow-hidden bg-gray-100 mb-3">
                <img :src="profilePicture" alt="Profile Picture" class="w-full h-full object-cover" />
              </div>
              <div v-else class="w-24 h-24 rounded-full bg-rose-gold/10 flex items-center justify-center mb-3">
                <Icon name="ph:user" class="w-12 h-12 text-rose-gold" />
              </div>
              <button 
                type="button"
                class="absolute bottom-0 right-0 bg-rose-gold text-white p-1.5 rounded-full shadow-md hover:bg-deep-maroon transition-colors"
              >
                <Icon name="ph:camera" class="w-4 h-4" />
              </button>
            </div>
            <p class="text-sm text-gray-500 mt-1">Click the camera icon to change your profile picture</p>
          </div>
          
          <!-- Form Fields -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <!-- First Name -->
            <div>
              <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">
                First Name
              </label>
              <input
                id="firstName"
                v-model="form.firstName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
                required
              />
            </div>
            
            <!-- Last Name -->
            <div>
              <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">
                Last Name
              </label>
              <input
                id="lastName"
                v-model="form.lastName"
                type="text"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
                required
              />
            </div>
            
            <!-- Email -->
            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 mb-1">
                Email Address
              </label>
              <input
                id="email"
                v-model="form.email"
                type="email"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-gray-50"
                disabled
              />
              <p class="text-xs text-gray-500 mt-1">Email cannot be changed</p>
            </div>
            
            <!-- Phone -->
            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">
                Phone Number
              </label>
              <input
                id="phone"
                v-model="form.phone"
                type="tel"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
              />
            </div>
            
            <!-- Date of Birth -->
            <div>
              <label for="dateOfBirth" class="block text-sm font-medium text-gray-700 mb-1">
                Date of Birth
              </label>
              <input
                id="dateOfBirth"
                v-model="form.dateOfBirth"
                type="date"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
              />
            </div>
            
            <!-- Gender -->
            <div>
              <label for="gender" class="block text-sm font-medium text-gray-700 mb-1">
                Gender
              </label>
              <select
                id="gender"
                v-model="form.gender"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
              >
                <option value="">Select Gender</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
                <option value="other">Other</option>
                <option value="prefer_not_to_say">Prefer not to say</option>
              </select>
            </div>
          </div>
          
          <!-- Preferences -->
          <div class="mb-6">
            <h3 class="text-lg font-medium text-gray-900 mb-3">Preferences</h3>
            
            <div class="space-y-3">
              <!-- Newsletter Subscription -->
              <div class="flex items-start">
                <div class="flex items-center h-5">
                  <input
                    id="newsletter"
                    v-model="form.preferences.newsletter"
                    type="checkbox"
                    class="h-4 w-4 text-rose-gold focus:ring-rose-gold border-gray-300 rounded"
                  />
                </div>
                <div class="ml-3 text-sm">
                  <label for="newsletter" class="font-medium text-gray-700">Subscribe to Newsletter</label>
                  <p class="text-gray-500">Receive updates about new products, offers, and events</p>
                </div>
              </div>
              
              <!-- Jewelry Style Preferences -->
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-2">
                  Preferred Jewelry Styles
                </label>
                <div class="grid grid-cols-2 gap-2">
                  <div v-for="style in jewelryStyles" :key="style.value" class="flex items-center">
                    <input
                      :id="`style-${style.value}`"
                      v-model="form.preferences.jewelryStyles"
                      type="checkbox"
                      :value="style.value"
                      class="h-4 w-4 text-rose-gold focus:ring-rose-gold border-gray-300 rounded"
                    />
                    <label :for="`style-${style.value}`" class="ml-2 text-sm text-gray-700">
                      {{ style.label }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Submit Button -->
          <div class="flex justify-end">
            <button
              type="submit"
              :disabled="isLoading"
              class="px-6 py-2 border border-transparent rounded-md shadow-sm text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            >
              <Icon
                v-if="isLoading"
                name="ph:circle-notch"
                class="animate-spin -ml-1 mr-2 h-4 w-4"
              />
              {{ isLoading ? 'Saving...' : 'Save Changes' }}
            </button>
          </div>
        </form>
      </div>
      
      <!-- Back to Dashboard Link -->
      <div class="mt-6 text-center">
        <NuxtLink to="/dashboard" class="text-rose-gold hover:text-deep-maroon transition-colors inline-flex items-center">
          <Icon name="ph:arrow-left" class="mr-1 h-4 w-4" />
          Back to Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useToast } from 'vue-toastification';

// SEO
useHead({
  title: 'My Profile - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Manage your Nakhrali Fashion profile and account preferences.'
    }
  ]
});

// Auth
const { user, updateProfile: updateUserProfile, isLoading } = useAuth();
const toast = useToast();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Profile picture
const profilePicture = ref('');

// Form data
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  dateOfBirth: '',
  gender: '',
  preferences: {
    newsletter: false,
    jewelryStyles: []
  }
});

// Jewelry styles options
const jewelryStyles = [
  { value: 'traditional', label: 'Traditional' },
  { value: 'contemporary', label: 'Contemporary' },
  { value: 'bridal', label: 'Bridal' },
  { value: 'minimalist', label: 'Minimalist' },
  { value: 'statement', label: 'Statement' },
  { value: 'vintage', label: 'Vintage' },
];

// Load user data
onMounted(async () => {
  if (user.value) {
    // Fill basic user info
    form.firstName = user.value.first_name || '';
    form.lastName = user.value.last_name || '';
    form.email = user.value.email || '';
    form.phone = user.value.phone || '';
    
    try {
      // Fetch detailed profile
      const response = await $fetch(`${apiBase}/auth/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      });
      
      if (response.profile) {
        // Fill profile data
        form.dateOfBirth = response.profile.date_of_birth ? response.profile.date_of_birth.substring(0, 10) : '';
        form.gender = response.profile.gender || '';
        
        // Fill preferences
        if (response.profile.preferences) {
          form.preferences.newsletter = response.profile.preferences.newsletter || false;
          form.preferences.jewelryStyles = response.profile.preferences.jewelry_styles || [];
        }
        
        // Set profile picture
        if (response.profile.profile_picture) {
          profilePicture.value = response.profile.profile_picture;
        }
      }
    } catch (error) {
      console.error('Failed to load profile:', error);
      toast.error('Failed to load your profile information');
    }
  }
});

// Update profile
const updateProfile = async () => {
  try {
    // Prepare data for API
    const profileData = {
      first_name: form.firstName,
      last_name: form.lastName,
      phone: form.phone,
      date_of_birth: form.dateOfBirth,
      gender: form.gender,
      preferences: {
        newsletter: form.preferences.newsletter,
        jewelry_styles: form.preferences.jewelryStyles
      }
    };
    
    // Call API to update profile
    await updateUserProfile(profileData);
    
    toast.success('Profile updated successfully');
  } catch (error) {
    console.error('Failed to update profile:', error);
    toast.error('Failed to update your profile');
  }
};

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
});
</script>