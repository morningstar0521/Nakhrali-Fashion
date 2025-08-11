<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-rose-gold/10">
          <Icon name="ph:lock-key" class="h-8 w-8 text-rose-gold" />
        </div>
        <h2 class="mt-6 text-3xl font-display font-bold text-deep-maroon">
          Forgot Password?
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Enter your email address and we'll send you a link to reset your password
        </p>
      </div>

      <!-- Success Message -->
      <div v-if="emailSent" class="bg-green-50 border border-green-200 rounded-lg p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <Icon name="ph:check-circle" class="h-5 w-5 text-green-400" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-green-800">
              Reset link sent!
            </h3>
            <div class="mt-2 text-sm text-green-700">
              <p>
                We've sent a password reset link to <strong>{{ form.email }}</strong>. 
                Please check your email and follow the instructions to reset your password.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Reset Form -->
      <form v-else class="mt-8 space-y-6" @submit.prevent="handleForgotPassword">
        <div class="space-y-4">
          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Icon name="ph:envelope" class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="email"
                v-model="form.email"
                name="email"
                type="email"
                autocomplete="email"
                required
                class="input-field pl-10"
                :class="{ 'border-red-500': errors.email }"
                placeholder="Enter your email address"
              />
            </div>
            <p v-if="errors.email" class="mt-1 text-sm text-red-600">
              {{ errors.email }}
            </p>
          </div>

          <!-- Submit Button -->
          <div>
            <button
              type="submit"
              :disabled="isLoading"
              class="btn-primary w-full flex justify-center items-center"
            >
              <Icon
                v-if="isLoading"
                name="ph:circle-notch"
                class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
              />
              {{ isLoading ? 'Sending...' : 'Send Reset Link' }}
            </button>
          </div>
        </div>

        <!-- Back to Login -->
        <div class="text-center">
          <p class="text-sm text-gray-600">
            Remember your password?
            <NuxtLink
              to="/auth/login"
              class="font-medium text-rose-gold hover:text-deep-maroon transition-colors"
            >
              Sign in here
            </NuxtLink>
          </p>
        </div>
      </form>

      <!-- Help Section -->
      <div class="mt-8 bg-gray-50 rounded-lg p-4">
        <h3 class="text-sm font-medium text-gray-900 mb-2">Need help?</h3>
        <p class="text-sm text-gray-600 mb-3">
          If you're having trouble accessing your account, you can:
        </p>
        <ul class="text-sm text-gray-600 space-y-1">
          <li class="flex items-start">
            <Icon name="ph:check" class="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
            Check your spam folder for the reset email
          </li>
          <li class="flex items-start">
            <Icon name="ph:check" class="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
            Contact our support team for assistance
          </li>
          <li class="flex items-start">
            <Icon name="ph:check" class="h-4 w-4 text-green-500 mr-2 mt-0.5 flex-shrink-0" />
            Try signing in with a different email address
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useToast } from 'vue-toastification'

// SEO
useHead({
  title: 'Forgot Password - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Reset your Nakhrali Fashion account password. Enter your email to receive a secure password reset link.'
    }
  ]
})

const { forgotPassword, isLoading } = useAuth()
const toast = useToast()

// Form data
const form = reactive({
  email: ''
})

// Form state
const emailSent = ref(false)
const errors = reactive({
  email: ''
})

// Validation
const validateForm = () => {
  errors.email = ''

  if (!form.email) {
    errors.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Please enter a valid email address'
  }

  return !errors.email
}

// Forgot password handler
const handleForgotPassword = async () => {
  if (!validateForm()) return

  try {
    await forgotPassword(form.email)
    emailSent.value = true
    toast.success('Password reset link has been sent to your email!')
  } catch (error) {
    console.error('Forgot password error:', error)
    
    if (error.response?.status === 404) {
      toast.error('No account found with this email address.')
    } else if (error.response?.status === 422) {
      const validationErrors = error.response._data?.errors
      if (validationErrors) {
        Object.keys(validationErrors).forEach(key => {
          if (form[key] !== undefined) {
            errors[key] = validationErrors[key][0]
          }
        })
      }
    } else {
      toast.error('An error occurred. Please try again later.')
    }
  }
}

// Auto-fill demo email for development
const fillDemoEmail = () => {
  if (process.env.NODE_ENV === 'development') {
    form.email = 'demo@nakhrali.com'
  }
}

// Fill demo email on mount in development
onMounted(() => {
  fillDemoEmail()
})

// Apply guest middleware
definePageMeta({
  middleware: 'guest'
})
</script>

<style scoped>
.input-field {
  @apply appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm transition-all duration-200;
}

.btn-primary {
  @apply relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed;
}
</style> 