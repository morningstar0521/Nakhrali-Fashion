<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8 bg-white p-8 rounded-lg shadow-md">
      <div class="text-center">
        <h2 class="mt-6 text-3xl font-display font-bold text-deep-maroon">
          Register Test
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Testing direct API connection for registration
        </p>
      </div>

      <div class="mt-8 space-y-6">
        <div class="space-y-4">
          <div>
            <label for="firstName" class="block text-sm font-medium text-gray-700 mb-2">
              First Name
            </label>
            <input
              id="firstName"
              v-model="firstName"
              type="text"
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm"
              placeholder="Enter your first name"
            />
          </div>

          <div>
            <label for="lastName" class="block text-sm font-medium text-gray-700 mb-2">
              Last Name
            </label>
            <input
              id="lastName"
              v-model="lastName"
              type="text"
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm"
              placeholder="Enter your last name"
            />
          </div>

          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <input
              id="email"
              v-model="email"
              type="email"
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm"
              placeholder="Enter your email"
            />
          </div>

          <div>
            <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
              Phone Number
            </label>
            <input
              id="phone"
              v-model="phone"
              type="tel"
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm"
              placeholder="Enter your phone number"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              class="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div>
          <button
            @click="testRegister"
            :disabled="isLoading"
            class="relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Icon
              v-if="isLoading"
              name="ph:circle-notch"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            />
            {{ isLoading ? 'Testing...' : 'Test Register' }}
          </button>
        </div>

        <div v-if="result" class="mt-4 p-4 rounded-lg" :class="result.success ? 'bg-green-50' : 'bg-red-50'">
          <h3 class="text-lg font-medium" :class="result.success ? 'text-green-800' : 'text-red-800'">
            {{ result.success ? 'Success!' : 'Error!' }}
          </h3>
          <pre class="mt-2 text-sm whitespace-pre-wrap" :class="result.success ? 'text-green-700' : 'text-red-700'">
            {{ JSON.stringify(result.data, null, 2) }}
          </pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toastification';

const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const toast = useToast();

const firstName = ref('Test');
const lastName = ref('User');
const email = ref('test' + Math.floor(Math.random() * 10000) + '@example.com');
const phone = ref('1234567890');
const password = ref('password123');
const isLoading = ref(false);
const result = ref(null);

async function testRegister() {
  isLoading.value = true;
  result.value = null;
  
  try {
    console.log('Testing registration with API base:', apiBase);
    console.log('Registration data:', { 
      first_name: firstName.value,
      last_name: lastName.value,
      email: email.value,
      phone: phone.value,
      password: password.value 
    });
    
    const response = await $fetch(`${apiBase}/auth/register`, {
      method: 'POST',
      body: {
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value,
        phone: phone.value,
        password: password.value
      }
    });
    
    console.log('Registration response:', response);
    
    result.value = {
      success: true,
      data: response
    };
    
    toast.success('Registration test successful!');
  } catch (error) {
    console.error('Registration test error:', error);
    
    result.value = {
      success: false,
      data: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?._data
      }
    };
    
    toast.error('Registration test failed!');
  } finally {
    isLoading.value = false;
  }
}
</script>