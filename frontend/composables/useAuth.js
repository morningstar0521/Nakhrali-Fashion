import { ref, computed, readonly } from 'vue'

export const useAuth = () => {
  // Get runtime config
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const accessToken = ref(null)
  const refreshToken = ref(null)

  // Computed
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'superadmin')
  const isSuperAdmin = computed(() => user.value?.role === 'superadmin')
  const userFullName = computed(() => {
    if (!user.value) return ''
    return `${user.value.first_name} ${user.value.last_name}`.trim()
  })

  // Initialize auth state from localStorage
  const initializeAuth = () => {
    try {
      const storedToken = localStorage.getItem('access_token')
      const storedRefreshToken = localStorage.getItem('refresh_token')
      const storedUser = localStorage.getItem('user')

      if (storedToken && storedUser) {
        accessToken.value = storedToken
        refreshToken.value = storedRefreshToken
        user.value = JSON.parse(storedUser)
        isAuthenticated.value = true
      }
    } catch (error) {
      console.error('Error initializing auth:', error)
      clearAuth()
    }
  }

  // Login
  const login = async (credentials) => {
    isLoading.value = true
    
    try {
      console.log('Attempting login with:', credentials)
      const response = await $fetch(`${apiBase}/auth/login`, {
        method: 'POST',
        body: credentials
      })

      console.log('Login response:', response)

      if (response.access_token) {
        accessToken.value = response.access_token
        refreshToken.value = response.refresh_token
        user.value = response.user
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))

        return { success: true }
      }
    } catch (error) {
      console.error('Login error:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // Google OAuth login
  const googleLogin = async (token) => {
    isLoading.value = true
    
    try {
      console.log('Attempting Google login with token')
      const response = await $fetch(`${apiBase}/auth/google`, {
        method: 'POST',
        body: { token }
      })

      console.log('Google login response:', response)

      if (response.access_token) {
        accessToken.value = response.access_token
        refreshToken.value = response.refresh_token
        user.value = response.user
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))

        return { success: true }
      }
    } catch (error) {
      console.error('Google login error:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // Register
  const register = async (userData) => {
    isLoading.value = true
    
    try {
      console.log('Attempting registration with:', userData)
      const response = await $fetch(`${apiBase}/auth/register`, {
        method: 'POST',
        body: userData
      })

      console.log('Registration response:', response)

      if (response.access_token) {
        accessToken.value = response.access_token
        refreshToken.value = response.refresh_token
        user.value = response.user
        isAuthenticated.value = true

        // Store in localStorage
        localStorage.setItem('access_token', response.access_token)
        localStorage.setItem('refresh_token', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))

        return { success: true }
      }
    } catch (error) {
      console.error('Registration error:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // Logout
  const logout = async () => {
    try {
      // Call logout endpoint if available
      if (accessToken.value) {
        await $fetch(`${apiBase}/auth/logout`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          }
        })
      }
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      clearAuth()
    }
  }

  // Refresh token
  const refreshAccessToken = async () => {
    if (!refreshToken.value) {
      throw new Error('No refresh token available')
    }

    try {
      const response = await $fetch(`${apiBase}/auth/refresh`, {
        method: 'POST',
        body: {
          refresh_token: refreshToken.value
        }
      })

      if (response.access_token) {
        accessToken.value = response.access_token
        localStorage.setItem('access_token', response.access_token)
        return response.access_token
      }
    } catch (error) {
      console.error('Token refresh error:', error)
      clearAuth()
      throw error
    }
  }

  // Update user profile
  const updateProfile = async (profileData) => {
    if (!isAuthenticated.value) {
      throw new Error('User not authenticated')
    }

    try {
      const response = await $fetch(`${apiBase}/auth/profile`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: profileData
      })

      if (response.user) {
        user.value = response.user
        localStorage.setItem('user', JSON.stringify(response.user))
        return response.user
      }
    } catch (error) {
      console.error('Profile update error:', error)
      throw error
    }
  }

  // Change password
  const changePassword = async (passwordData) => {
    if (!isAuthenticated.value) {
      throw new Error('User not authenticated')
    }

    try {
      await $fetch(`${apiBase}/auth/change-password`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: passwordData
      })

      return { success: true }
    } catch (error) {
      console.error('Password change error:', error)
      throw error
    }
  }

  // Forgot password
  const forgotPassword = async (email) => {
    try {
      await $fetch(`${apiBase}/auth/forgot-password`, {
        method: 'POST',
        body: { email }
      })

      return { success: true }
    } catch (error) {
      console.error('Forgot password error:', error)
      throw error
    }
  }

  // Reset password
  const resetPassword = async (token, password) => {
    try {
      await $fetch(`${apiBase}/auth/reset-password`, {
        method: 'POST',
        body: { token, password }
      })

      return { success: true }
    } catch (error) {
      console.error('Reset password error:', error)
      throw error
    }
  }

  // Clear auth state
  const clearAuth = () => {
    user.value = null
    isAuthenticated.value = false
    accessToken.value = null
    refreshToken.value = null

    // Clear localStorage
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user')
  }

  // Get auth headers for API calls
  const getAuthHeaders = () => {
    if (!accessToken.value) {
      return {}
    }
    return {
      'Authorization': `Bearer ${accessToken.value}`
    }
  }

  // Check if token is expired
  const isTokenExpired = (token) => {
    if (!token) return true
    
    try {
      const payload = JSON.parse(atob(token.split('.')[1]))
      const currentTime = Date.now() / 1000
      return payload.exp < currentTime
    } catch (error) {
      return true
    }
  }

  // Auto-refresh token if needed
  const ensureValidToken = async () => {
    if (!accessToken.value) {
      return false
    }

    if (isTokenExpired(accessToken.value)) {
      try {
        await refreshAccessToken()
        return true
      } catch (error) {
        clearAuth()
        return false
      }
    }

    return true
  }

  // Initialize on mount
  if (process.client) {
    initializeAuth()
  }

  return {
    // State
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    isLoading: readonly(isLoading),
    accessToken: readonly(accessToken),
    
    // Computed
    isAdmin: readonly(isAdmin),
    isSuperAdmin: readonly(isSuperAdmin),
    userFullName: readonly(userFullName),
    
    // Methods
    login,
    googleLogin,
    register,
    logout,
    refreshAccessToken,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    clearAuth,
    getAuthHeaders,
    ensureValidToken,
    initializeAuth
  }
}