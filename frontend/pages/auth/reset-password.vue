<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-rose-gold/10">
          <Icon name="ph:lock-key" class="h-8 w-8 text-rose-gold" />
        </div>
        <h2 class="mt-6 text-3xl font-display font-bold text-deep-maroon">
          Reset Your Password
        </h2>
        <p class="mt-2 text-sm text-gray-600">
          Enter your new password below
        </p>
      </div>

      <!-- Error Message -->
      <div v-if="tokenError" class="bg-red-50 border border-red-200 rounded-lg p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <Icon name="ph:warning-circle" class="h-5 w-5 text-red-400" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-red-800">
              Invalid or expired reset link
            </h3>
            <div class="mt-2 text-sm text-red-700">
              <p>
                This password reset link is invalid or has expired. Please request a new one.
              </p>
            </div>
            <div class="mt-4">
              <NuxtLink
                to="/auth/forgot-password"
                class="text-sm font-medium text-red-800 hover:text-red-700"
              >
                Request new reset link →
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Success Message -->
      <div v-else-if="passwordReset" class="bg-green-50 border border-green-200 rounded-lg p-4">
        <div class="flex">
          <div class="flex-shrink-0">
            <Icon name="ph:check-circle" class="h-5 w-5 text-green-400" />
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-green-800">
              Password reset successful!
            </h3>
            <div class="mt-2 text-sm text-green-700">
              <p>
                Your password has been successfully reset. You can now sign in with your new password.
              </p>
            </div>
            <div class="mt-4">
              <NuxtLink
                to="/auth/login"
                class="btn-primary inline-flex items-center"
              >
                Sign In
                <Icon name="ph:arrow-right" class="ml-2 h-4 w-4" />
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>

      <!-- Reset Form -->
      <form v-else class="mt-8 space-y-6" @submit.prevent="handleResetPassword">
        <div class="space-y-4">
          <!-- New Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              New Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Icon name="ph:lock" class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="input-field pl-10 pr-10"
                :class="{ 'border-red-500': errors.password }"
                placeholder="Enter your new password"
              />
              <button
                type="button"
                @click="showPassword = !showPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <Icon
                  :name="showPassword ? 'ph:eye-slash' : 'ph:eye'"
                  class="h-5 w-5 text-gray-400 hover:text-gray-600"
                />
              </button>
            </div>
            <p v-if="errors.password" class="mt-1 text-sm text-red-600">
              {{ errors.password }}
            </p>
          </div>

          <!-- Confirm Password Field -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirm New Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Icon name="ph:lock" class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                class="input-field pl-10 pr-10"
                :class="{ 'border-red-500': errors.confirmPassword }"
                placeholder="Confirm your new password"
              />
              <button
                type="button"
                @click="showConfirmPassword = !showConfirmPassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center"
              >
                <Icon
                  :name="showConfirmPassword ? 'ph:eye-slash' : 'ph:eye'"
                  class="h-5 w-5 text-gray-400 hover:text-gray-600"
                />
              </button>
            </div>
            <p v-if="errors.confirmPassword" class="mt-1 text-sm text-red-600">
              {{ errors.confirmPassword }}
            </p>
          </div>

          <!-- Password Strength Indicator -->
          <div class="mt-4">
            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">Password strength:</span>
              <span :class="passwordStrength.color">{{ passwordStrength.text }}</span>
            </div>
            <div class="mt-2 w-full bg-gray-200 rounded-full h-2">
              <div
                class="h-2 rounded-full transition-all duration-300"
                :class="passwordStrength.color"
                :style="{ width: passwordStrength.percentage + '%' }"
              ></div>
            </div>
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
              {{ isLoading ? 'Resetting...' : 'Reset Password' }}
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
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

// SEO
useHead({
  title: 'Reset Password - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Reset your Nakhrali Fashion account password with a secure token.'
    }
  ]
})

const route = useRoute()
const { resetPassword, isLoading } = useAuth()
const toast = useToast()

// Form data
const form = reactive({
  password: '',
  confirmPassword: ''
})

// Form state
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const tokenError = ref(false)
const passwordReset = ref(false)
const errors = reactive({
  password: '',
  confirmPassword: ''
})

// Get token from route
const token = route.query.token

// Password strength calculation
const passwordStrength = computed(() => {
  const password = form.password
  if (!password) return { text: '', percentage: 0, color: 'bg-gray-200' }
  
  let score = 0
  
  if (password.length >= 8) score += 25
  if (/[a-z]/.test(password)) score += 25
  if (/[A-Z]/.test(password)) score += 25
  if (/[0-9]/.test(password)) score += 25
  if (/[^A-Za-z0-9]/.test(password)) score += 25
  
  if (score <= 25) {
    return { text: 'Weak', percentage: score, color: 'bg-red-500' }
  } else if (score <= 50) {
    return { text: 'Fair', percentage: score, color: 'bg-yellow-500' }
  } else if (score <= 75) {
    return { text: 'Good', percentage: score, color: 'bg-blue-500' }
  } else {
    return { text: 'Strong', percentage: score, color: 'bg-green-500' }
  }
})

// Validation
const validateForm = () => {
  errors.password = ''
  errors.confirmPassword = ''

  if (!form.password) {
    errors.password = 'Password is required'
  } else if (form.password.length < 8) {
    errors.password = 'Password must be at least 8 characters'
  }

  if (!form.confirmPassword) {
    errors.confirmPassword = 'Please confirm your password'
  } else if (form.password !== form.confirmPassword) {
    errors.confirmPassword = 'Passwords do not match'
  }

  return !errors.password && !errors.confirmPassword
}

// Reset password handler
const handleResetPassword = async () => {
  if (!validateForm()) return

  try {
    await resetPassword(token, form.password)
    passwordReset.value = true
    toast.success('Password reset successful!')
  } catch (error) {
    console.error('Reset password error:', error)
    
    if (error.response?.status === 400) {
      tokenError.value = true
      toast.error('Invalid or expired reset token.')
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

// Check token validity on mount
onMounted(async () => {
  if (!token) {
    tokenError.value = true
    return
  }

  try {
    // Validate token with backend
    await $fetch('/api/auth/validate-reset-token', {
      method: 'POST',
      body: { token }
    })
  } catch (error) {
    if (error.response?.status === 400) {
      tokenError.value = true
    }
  }
})
</script>

<style scoped>
.input-field {
  @apply appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold focus:z-10 sm:text-sm transition-all duration-200;
}

.btn-primary {
  @apply relative flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed;
}
</style> 