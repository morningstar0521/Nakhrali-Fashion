<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Logo and Header -->
      <div class="text-center">
        <div class="mx-auto h-16 w-16 flex items-center justify-center rounded-full bg-rose-gold/10">
          <Icon name="ph:crown" class="h-8 w-8 text-rose-gold" />
        </div>
        <h2 class="mt-6 text-3xl font-display font-bold text-deep-maroon dark:text-rose-gold">
          Welcome Back
        </h2>
        <p class="mt-2 text-sm text-gray-600 dark:text-gray-400">
          Sign in to your Nakhrali Fashion account
        </p>
      </div>

      <!-- Login Form -->
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="space-y-4">
          <!-- Email Field -->
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
                name="email"
                type="email"
                autocomplete="email"
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

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Icon name="ph:lock" class="h-5 w-5 text-gray-400" />
              </div>
              <input
                id="password"
                v-model="form.password"
                name="password"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="current-password"
                required
                class="input-field pl-10 pr-10"
                :class="{ 'border-red-500': errors.password }"
                placeholder="Enter your password"
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
          
          <!-- Google Login Button -->
          <div class="mt-6">
            <button
              type="button"
              @click="handleGoogleLogin"
              class="w-full flex items-center justify-center px-4 py-3 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-colors"
            >
              <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" alt="Google" class="w-5 h-5 mr-2" />
              Sign in with Google
            </button>
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                v-model="form.rememberMe"
                name="remember-me"
                type="checkbox"
                class="h-4 w-4 text-rose-gold focus:ring-rose-gold border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-gray-700 dark:text-gray-300">
                Remember me
              </label>
            </div>

            <div class="text-sm">
              <NuxtLink to="/auth/forgot-password" class="font-medium text-rose-gold hover:text-deep-maroon">
                Forgot your password?
              </NuxtLink>
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <div>
          <button
            type="submit"
            :disabled="isLoading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-colors"
          >
            <span v-if="isLoading" class="flex items-center">
              <Icon name="ph:spinner" class="animate-spin h-5 w-5 mr-2" />
              Signing in...
            </span>
            <span v-else>Sign in</span>
          </button>
        </div>
      </form>

      <!-- Register Link -->
      <div class="text-center mt-4">
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Don't have an account?
          <NuxtLink to="/auth/register" class="font-medium text-rose-gold hover:text-deep-maroon">
            Sign up
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Login - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Sign in to your Nakhrali Fashion account to access your dashboard, orders, and more.'
    }
  ]
})

// Auth composable
const { login, googleLogin, isLoading } = useAuth()
const router = useRouter()
const route = useRoute()

// Form state
const form = ref({
  email: '',
  password: '',
  rememberMe: false
})

const errors = ref({
  email: '',
  password: '',
  general: ''
})

const showPassword = ref(false)

// Handle login
const handleLogin = async () => {
  // Clear previous errors
  errors.value = {
    email: '',
    password: '',
    general: ''
  }

  // Basic validation
  if (!form.value.email) {
    errors.value.email = 'Email is required'
    return
  }

  if (!form.value.password) {
    errors.value.password = 'Password is required'
    return
  }

  try {
    const result = await login({
      email: form.value.email,
      password: form.value.password
    })

    if (result.success) {
      // Redirect to intended destination or dashboard
      const redirectPath = route.query.redirect || '/dashboard'
      router.push(redirectPath)
    }
  } catch (error) {
    console.error('Login error:', error)
    
    if (error.response) {
      const { status, data } = error.response
      
      if (status === 401) {
        errors.value.general = 'Invalid email or password'
      } else if (status === 403) {
        errors.value.general = 'Your account is inactive'
      } else if (data && data.error) {
        errors.value.general = data.error
      } else {
        errors.value.general = 'An error occurred during login'
      }
    } else {
      errors.value.general = 'Unable to connect to the server'
    }
  }
}

// Handle Google login
const handleGoogleLogin = async () => {
  // In a real implementation, this would use Google OAuth
  // For now, we'll just show a message
  alert('Google login is not implemented in this demo')
}
</script>

<style scoped>
.input-field {
  @apply appearance-none block w-full px-3 py-3 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-rose-gold focus:border-rose-gold dark:bg-gray-800 dark:text-white text-sm;
}
</style>