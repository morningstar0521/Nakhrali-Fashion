<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-rose-gold/10">
          <Icon name="ph:crown" class="h-8 w-8 text-rose-gold" />
        </div>
        <h2 class="mt-6 text-3xl font-display font-bold text-deep-maroon dark:text-rose-gold">
          Join Nakhrali Fashion
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Create your account to start your jewelry journey
        </p>
      </div>

      <!-- Registration Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleFormSubmit">
        <div class="space-y-4">
          <!-- Google Registration Button -->
          <div class="mb-6">
            <button
              type="button"
              @click="socialLogin('google')"
              class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-colors"
            >
              <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" class="w-5 h-5 mr-2" />
              Sign up with Google
            </button>
            <div class="relative my-6">
              <div class="absolute inset-0 flex items-center">
                <div class="w-full border-t border-gray-300 dark:border-gray-700"></div>
              </div>
              <div class="relative flex justify-center text-sm">
                <span class="px-2 bg-gradient-to-br from-ivory to-rose-gold/10 dark:from-gray-900 dark:to-gray-800 text-gray-500 dark:text-gray-400">Or continue with email</span>
              </div>
            </div>
          </div>
          <!-- Step Indicator -->
          <div class="flex items-center justify-center space-x-2 mb-6">
            <div
              v-for="(step, index) in steps"
              :key="index"
              class="flex items-center"
            >
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors"
                :class="currentStep >= index ? 'bg-rose-gold text-white' : 'bg-gray-200 text-gray-500'"
              >
                {{ index + 1 }}
              </div>
              <div
                v-if="index < steps.length - 1"
                class="w-8 h-1 mx-2 transition-colors"
                :class="currentStep > index ? 'bg-rose-gold' : 'bg-gray-200'"
              ></div>
            </div>
          </div>

          <!-- Debug Info (remove in production) -->
          <div class="mb-4 p-3 bg-rose-gold/10 border border-rose-gold/20 rounded-lg">
            <p class="text-sm font-medium text-deep-maroon">Current Step: {{ currentStep + 1 }} of {{ steps.length }}</p>
            <p class="text-sm text-gray-600">Step Name: {{ steps[currentStep] }}</p>
          </div>

          <!-- Step 1: Basic Information -->
          <div v-if="currentStep === 0" class="space-y-4">
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  First Name
                </label>
                <input
                  id="firstName"
                  v-model="form.firstName"
                  type="text"
                  required
                  class="input-field"
                  :class="{ 'border-red-500': errors.firstName }"
                  placeholder="First name"
                />
                <p v-if="errors.firstName" class="mt-1 text-sm text-red-600">
                  {{ errors.firstName }}
                </p>
              </div>
              <div>
                <label for="lastName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Last Name
                </label>
                <input
                  id="lastName"
                  v-model="form.lastName"
                  type="text"
                  required
                  class="input-field"
                  :class="{ 'border-red-500': errors.lastName }"
                  placeholder="Last name"
                />
                <p v-if="errors.lastName" class="mt-1 text-sm text-red-600">
                  {{ errors.lastName }}
                </p>
              </div>
            </div>

            <div>
              <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email Address
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Icon name="ph:envelope" class="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  required
                  class="input-field pl-10"
                  :class="{ 'border-red-500': errors.email }"
                  placeholder="Enter your email"
                />
              </div>
              <p v-if="errors.email" class="mt-1 text-sm text-red-600">
                {{ errors.email }}
              </p>
            </div>

            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Phone Number
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Icon name="ph:phone" class="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="phone"
                  v-model="form.phone"
                  type="tel"
                  required
                  class="input-field pl-10"
                  :class="{ 'border-red-500': errors.phone }"
                  placeholder="Enter your phone number"
                />
              </div>
              <p v-if="errors.phone" class="mt-1 text-sm text-red-600">
                {{ errors.phone }}
              </p>
            </div>
          </div>

          <!-- Step 2: Password -->
          <div v-if="currentStep === 1" class="space-y-4">
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Password
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
                  placeholder="Create a password"
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

            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
                Confirm Password
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
                  placeholder="Confirm your password"
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
          </div>

          <!-- Step 3: Preferences -->
          <div v-if="currentStep === 2" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Date of Birth
              </label>
              <input
                v-model="form.dateOfBirth"
                type="date"
                class="input-field"
                :class="{ 'border-red-500': errors.dateOfBirth }"
              />
              <p v-if="errors.dateOfBirth" class="mt-1 text-sm text-red-600">
                {{ errors.dateOfBirth }}
              </p>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Gender
              </label>
              <div class="grid grid-cols-3 gap-3">
                <label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:border-rose-gold transition-colors">
                  <input
                    v-model="form.gender"
                    type="radio"
                    value="female"
                    class="sr-only"
                  />
                  <div class="w-4 h-4 border-2 border-gray-300 rounded-full mr-2 flex items-center justify-center">
                    <div v-if="form.gender === 'female'" class="w-2 h-2 bg-rose-gold rounded-full"></div>
                  </div>
                  <span class="text-sm">Female</span>
                </label>
                <label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:border-rose-gold transition-colors">
                  <input
                    v-model="form.gender"
                    type="radio"
                    value="male"
                    class="sr-only"
                  />
                  <div class="w-4 h-4 border-2 border-gray-300 rounded-full mr-2 flex items-center justify-center">
                    <div v-if="form.gender === 'male'" class="w-2 h-2 bg-rose-gold rounded-full"></div>
                  </div>
                  <span class="text-sm">Male</span>
                </label>
                <label class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:border-rose-gold transition-colors">
                  <input
                    v-model="form.gender"
                    type="radio"
                    value="other"
                    class="sr-only"
                  />
                  <div class="w-4 h-4 border-2 border-gray-300 rounded-full mr-2 flex items-center justify-center">
                    <div v-if="form.gender === 'other'" class="w-2 h-2 bg-rose-gold rounded-full"></div>
                  </div>
                  <span class="text-sm">Other</span>
                </label>
              </div>
            </div>

            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Preferred Jewelry Style
              </label>
              <div class="grid grid-cols-2 gap-3">
                <label
                  v-for="style in jewelryStyles"
                  :key="style.value"
                  class="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:border-rose-gold transition-colors"
                >
                  <input
                    v-model="form.preferredStyles"
                    type="checkbox"
                    :value="style.value"
                    class="sr-only"
                  />
                  <div class="w-4 h-4 border-2 border-gray-300 rounded mr-2 flex items-center justify-center">
                    <Icon
                      v-if="form.preferredStyles.includes(style.value)"
                      name="ph:check"
                      class="w-3 h-3 text-white"
                    />
                  </div>
                  <span class="text-sm">{{ style.label }}</span>
                </label>
              </div>
            </div>

            <div class="flex items-center">
              <input
                id="newsletter"
                v-model="form.newsletter"
                type="checkbox"
                class="h-4 w-4 text-rose-gold focus:ring-rose-gold border-gray-300 rounded"
              />
              <label for="newsletter" class="ml-2 block text-sm text-gray-700">
                Subscribe to our newsletter for exclusive offers and updates
              </label>
            </div>

            <div class="flex items-center">
              <input
                id="terms"
                v-model="form.agreeToTerms"
                type="checkbox"
                required
                class="h-4 w-4 text-rose-gold focus:ring-rose-gold border-gray-300 rounded"
              />
              <label for="terms" class="ml-2 block text-sm text-gray-700">
                I agree to the
                <NuxtLink to="/terms" class="text-rose-gold hover:text-deep-maroon">
                  Terms of Service
                </NuxtLink>
                and
                <NuxtLink to="/privacy" class="text-rose-gold hover:text-deep-maroon">
                  Privacy Policy
                </NuxtLink>
              </label>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex justify-between">
          <button
            v-if="currentStep > 0"
            type="button"
            @click="previousStep"
            class="btn-secondary"
          >
            Previous
          </button>
          <div v-else></div>

          <button
            v-if="currentStep < steps.length - 1"
            type="button"
            @click="nextStep"
            :disabled="isLoading"
            class="btn-primary flex items-center"
          >
            <Icon
              v-if="isLoading"
              name="ph:circle-notch"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            />
            {{ isLoading ? 'Saving...' : 'Next' }}
          </button>
          <button
            v-else
            type="submit"
            :disabled="isLoading"
            class="btn-primary flex items-center"
          >
            <Icon
              v-if="isLoading"
              name="ph:circle-notch"
              class="animate-spin -ml-1 mr-3 h-5 w-5 text-white"
            />
            {{ isLoading ? 'Creating Account...' : 'Create Account' }}
          </button>
        </div>

        <!-- Validation Summary -->
        <div v-if="Object.values(errors).some(e => e && e.length > 0)" class="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
          <h4 class="text-sm font-medium text-red-800 mb-2">Please fix the following errors:</h4>
          <ul class="text-sm text-red-700 space-y-1">
            <li v-for="error in Object.values(errors).filter(e => e && e.length > 0)" :key="error">
              • {{ error }}
            </li>
          </ul>
        </div>

        <!-- Sign In Link -->
        <div class="text-center">
          <p class="text-sm text-gray-600">
            Already have an account?
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
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

// SEO
useHead({
  title: 'Sign Up - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Create your Nakhrali Fashion account to access exclusive jewelry collections, personalized recommendations, and special offers.'
    }
  ]
})

const router = useRouter()
const { register, isLoading } = useAuth()
const toast = useToast()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

// Google OAuth state
const googleAuthUrl = ref('')
const googleAuthWindow = ref(null)

// Initialize Google OAuth
onMounted(async () => {
  try {
    const response = await $fetch(`${apiBase}/auth/google/auth`, {
      method: 'GET'
    })
    
    if (response.auth_url) {
      googleAuthUrl.value = response.auth_url
    }
  } catch (error) {
    console.error('Failed to initialize Google OAuth:', error)
  }
})

// Handle Google login/registration
async function socialLogin(provider) {
  if (provider !== 'google' || !googleAuthUrl.value) {
    toast.error(`${provider} authentication is not available`)
    return
  }
  
  // Open Google OAuth popup
  const width = 500
  const height = 600
  const left = window.screenX + (window.outerWidth - width) / 2
  const top = window.screenY + (window.outerHeight - height) / 2
  
  googleAuthWindow.value = window.open(
    googleAuthUrl.value,
    'Google Login',
    `width=${width},height=${height},left=${left},top=${top}`
  )
  
  // Listen for messages from popup
  window.addEventListener('message', handleGoogleCallback, false)
}

// Handle Google callback
async function handleGoogleCallback(event) {
  // Verify origin for security
  const allowedOrigin = window.location.origin
  if (event.origin !== allowedOrigin) return
  
  // Process callback data
  const { code, state } = event.data
  
  if (code && state) {
    try {
      const response = await $fetch(`${apiBase}/auth/google/callback`, {
        method: 'POST',
        body: { code, state }
      })
      
      if (response.access_token) {
        // Store tokens and user data
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))
        
        // Update auth state
        const { initializeAuth } = useAuth()
        initializeAuth()
        
        toast.success('Google authentication successful!')
        router.push('/dashboard')
      }
    } catch (error) {
      console.error('Google authentication error:', error)
      toast.error('Google authentication failed')
    } finally {
      window.removeEventListener('message', handleGoogleCallback)
      if (googleAuthWindow.value) googleAuthWindow.value.close()
    }
  }
}

// Form steps
const steps = ['Basic Info', 'Password', 'Preferences']
const currentStep = ref(0)

// Form data
const form = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  dateOfBirth: '',
  gender: '',
  preferredStyles: [],
  newsletter: true,
  agreeToTerms: false
})

// Form state
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const errors = reactive({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  dateOfBirth: ''
})

// Jewelry styles
const jewelryStyles = [
  { value: 'traditional', label: 'Traditional' },
  { value: 'modern', label: 'Modern' },
  { value: 'bridal', label: 'Bridal' },
  { value: 'casual', label: 'Casual' },
  { value: 'luxury', label: 'Luxury' },
  { value: 'minimalist', label: 'Minimalist' }
]

// Password strength calculation
const passwordStrength = computed(() => {
  const password = form.password
  if (!password) return { text: '', percentage: 0, color: 'bg-gray-200' }
  
  let score = 0
  let feedback = []
  
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

// Validation functions
const validateStep = (step) => {
  clearErrors()
  console.log('Validating step:', step)
  
  if (step === 0) {
    console.log('Validating step 0 - Basic Info')
    if (!form.firstName) {
      errors.firstName = 'First name is required'
      console.log('First name error')
    }
    if (!form.lastName) {
      errors.lastName = 'Last name is required'
      console.log('Last name error')
    }
    if (!form.email) {
      errors.email = 'Email is required'
      console.log('Email error')
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
      errors.email = 'Please enter a valid email address'
      console.log('Email format error')
    }
    if (!form.phone) {
      errors.phone = 'Phone number is required'
      console.log('Phone error')
    } else if (!/^[0-9]{10}$/.test(form.phone.replace(/\D/g, ''))) {
      errors.phone = 'Please enter a valid 10-digit phone number'
      console.log('Phone format error')
    }
  } else if (step === 1) {
    console.log('Validating step 1 - Password')
    if (!form.password) {
      errors.password = 'Password is required'
      console.log('Password error')
    } else if (form.password.length < 8) {
      errors.password = 'Password must be at least 8 characters'
      console.log('Password length error')
    }
    if (!form.confirmPassword) {
      errors.confirmPassword = 'Please confirm your password'
      console.log('Confirm password error')
    } else if (form.password !== form.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match'
      console.log('Password match error')
    }
  } else if (step === 2) {
    console.log('Validating step 2 - Preferences')
    if (!form.agreeToTerms) {
      toast.error('Please agree to the Terms of Service and Privacy Policy')
      console.log('Terms agreement error')
      return false
    }
  }
  
  // Check if there are any errors
  const hasErrors = Object.values(errors).some(error => error && error.length > 0)
  console.log('Validation result:', !hasErrors, 'Errors:', Object.values(errors).filter(e => e && e.length > 0))
  return !hasErrors
}

const clearErrors = () => {
  Object.keys(errors).forEach(key => {
    errors[key] = ''
  })
}

// Navigation
const nextStep = () => {
  console.log('Next step clicked, current step:', currentStep.value)
  console.log('Form data:', form)
  if (validateStep(currentStep.value)) {
    console.log('Validation passed, moving to step:', currentStep.value + 1)
    currentStep.value++
  } else {
    console.log('Validation failed')
    toast.error('Please fix the errors before continuing')
  }
}

const previousStep = () => {
  currentStep.value--
}

// Registration handler
const handleRegister = async () => {
  if (!validateStep(currentStep.value)) return

  console.log('Starting registration process...')
  console.log('Registration data:', {
    first_name: form.firstName,
    last_name: form.lastName,
    email: form.email,
    phone: form.phone,
    date_of_birth: form.dateOfBirth,
    gender: form.gender,
    preferred_styles: form.preferredStyles,
    newsletter_subscription: form.newsletter
  })

  try {
    const result = await register({
      first_name: form.firstName,
      last_name: form.lastName,
      email: form.email,
      phone: form.phone,
      password: form.password,
      date_of_birth: form.dateOfBirth,
      gender: form.gender,
      preferred_styles: form.preferredStyles,
      newsletter_subscription: form.newsletter
    })
    
    console.log('Registration successful:', result)
    toast.success('🎉 Welcome to Nakhrali Fashion! Your account has been created successfully.')
    
    // Small delay to show success message
    setTimeout(async () => {
      await router.push('/')
    }, 1500)
    
  } catch (error) {
    console.error('Registration error:', error)
    
    // Handle different types of errors
    if (error.response?.status === 422) {
      const validationErrors = error.response.data?.errors || error.response._data?.errors
      if (validationErrors) {
        console.log('Validation errors received:', validationErrors)
        Object.keys(validationErrors).forEach(key => {
          const fieldMap = {
            'first_name': 'firstName',
            'last_name': 'lastName',
            'date_of_birth': 'dateOfBirth',
            'preferred_styles': 'preferredStyles',
            'newsletter_subscription': 'newsletter'
          }
          const field = fieldMap[key] || key
          if (errors.hasOwnProperty(field)) {
            errors[field] = Array.isArray(validationErrors[key]) 
              ? validationErrors[key][0] 
              : validationErrors[key]
          }
        })
        toast.error('Please fix the validation errors and try again.')
      } else {
        toast.error('Please check your information and try again.')
      }
    } else if (error.response?.status === 409) {
      // Check if the error message contains information about which field caused the conflict
      const errorMessage = error.response.data?.error || error.response._data?.error || ''
      
      if (errorMessage.includes('phone')) {
        errors.phone = 'An account with this phone number already exists'
        toast.error('An account with this phone number already exists. Please use a different phone number.')
      } else {
        // Default to email conflict if not specified
        errors.email = 'An account with this email already exists'
        toast.error('An account with this email already exists. Please sign in instead.')
      }
      // Go back to first step to show error
      currentStep.value = 0
    } else if (error.response?.status === 400) {
      const errorMessage = error.response.data?.error || error.response._data?.error || 'Invalid request'
      toast.error(errorMessage)
      
      // If it's a specific field error, try to show it on the first step
      if (errorMessage.includes('email')) {
        errors.email = errorMessage
        currentStep.value = 0
      } else if (errorMessage.includes('phone')) {
        errors.phone = errorMessage
        currentStep.value = 0
      } else if (errorMessage.includes('password')) {
        errors.password = errorMessage
        currentStep.value = 1
      }
    } else if (error.response?.status === 500) {
      toast.error('Server error. Please try again later or contact support.')
    } else if (error.code === 'NETWORK_ERROR' || !error.response) {
      toast.error('Network error. Please check your connection and try again.')
    } else {
      toast.error('An unexpected error occurred. Please try again later.')
    }
  }
}

// Form submit handler
const handleFormSubmit = (event) => {
  event.preventDefault()
  if (currentStep.value < steps.length - 1) {
    nextStep()
  } else {
    handleRegister()
  }
}

// Auto-fill demo data for development
const fillDemoData = () => {
  if (process.env.NODE_ENV === 'development') {
    form.firstName = 'Demo'
    form.lastName = 'User'
    form.email = 'demo@nakhrali.com'
    form.phone = '9876543210'
    form.password = 'password123'
    form.confirmPassword = 'password123'
    form.dateOfBirth = '1990-01-01'
    form.gender = 'female'
    form.preferredStyles = ['traditional', 'bridal']
    form.agreeToTerms = true
  }
}

// Fill demo data on mount in development
onMounted(() => {
  fillDemoData()
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
  @apply relative flex justify-center py-3 px-6 border border-transparent text-sm font-medium rounded-lg text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply relative flex justify-center py-3 px-6 border border-gray-300 text-sm font-medium rounded-lg text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-all duration-200;
}
</style>