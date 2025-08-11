import { ref, computed, watch } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuth } from './useAuth'
import { useRuntimeConfig } from '#app'

export const useWishlist = () => {
  const toast = useToast()
  const { getAuthHeaders, isAuthenticated, ensureValidToken } = useAuth()
  
  // State
  const wishlistItems = ref([])
  const isLoading = ref(false)
  const error = ref(null)
  
  // Computed
  const wishlistCount = computed(() => wishlistItems.value.length)
  const wishlistTotal = computed(() => {
    return wishlistItems.value.reduce((total, item) => {
      return total + parseFloat(item.product?.price || 0)
    }, 0)
  })
  
  // Check if a product is in the wishlist
  const isInWishlist = (productId) => {
    return wishlistItems.value.some(item => item.product_id === productId)
  }
  
  // Get wishlist item by product ID
  const getWishlistItem = (productId) => {
    return wishlistItems.value.find(item => item.product_id === productId)
  }
  
  // Load wishlist
  const loadWishlist = async () => {
    if (!isAuthenticated.value) {
      wishlistItems.value = []
      return
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      await ensureValidToken()
      const response = await fetch(`${useRuntimeConfig().public.apiBase}/wishlist`, {
        method: 'GET',
        headers: getAuthHeaders()
      })
      
      if (!response.ok) {
        throw new Error('Failed to load wishlist')
      }
      
      const data = await response.json()
      wishlistItems.value = data.items || []
    } catch (err) {
      console.error('Error loading wishlist:', err)
      error.value = err.message
      toast.error('Failed to load wishlist')
    } finally {
      isLoading.value = false
    }
  }
  
  // Add to wishlist
  const addToWishlist = async (product, variant = null) => {
    if (!isAuthenticated.value) {
      toast.info('Please login to add items to your wishlist')
      return false
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      await ensureValidToken()
      const response = await fetch(`${useRuntimeConfig().public.apiBase}/wishlist/add`, {
        method: 'POST',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: product.id,
          product_variant_id: variant?.id || null
        })
      })
      
      if (!response.ok) {
        throw new Error('Failed to add item to wishlist')
      }
      
      const data = await response.json()
      
      // Refresh wishlist
      await loadWishlist()
      
      toast.success('Item added to wishlist')
      return true
    } catch (err) {
      console.error('Error adding to wishlist:', err)
      error.value = err.message
      toast.error('Failed to add item to wishlist')
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  // Remove from wishlist
  const removeFromWishlist = async (itemId) => {
    if (!isAuthenticated.value) {
      return false
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      await ensureValidToken()
      const response = await fetch(`${useRuntimeConfig().public.apiBase}/wishlist/remove/${itemId}`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      })
      
      if (!response.ok) {
        throw new Error('Failed to remove item from wishlist')
      }
      
      // Refresh wishlist
      await loadWishlist()
      
      toast.success('Item removed from wishlist')
      return true
    } catch (err) {
      console.error('Error removing from wishlist:', err)
      error.value = err.message
      toast.error('Failed to remove item from wishlist')
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  // Toggle wishlist (add if not in wishlist, remove if already in wishlist)
  const toggleWishlist = async (product, variant = null) => {
    if (!isAuthenticated.value) {
      toast.info('Please login to manage your wishlist')
      return false
    }
    
    const existingItem = getWishlistItem(product.id)
    
    if (existingItem) {
      return await removeFromWishlist(existingItem.id)
    } else {
      return await addToWishlist(product, variant)
    }
  }
  
  // Clear wishlist
  const clearWishlist = async () => {
    if (!isAuthenticated.value) {
      return false
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      await ensureValidToken()
      const response = await fetch(`${useRuntimeConfig().public.apiBase}/wishlist/clear`, {
        method: 'DELETE',
        headers: getAuthHeaders()
      })
      
      if (!response.ok) {
        throw new Error('Failed to clear wishlist')
      }
      
      wishlistItems.value = []
      toast.success('Wishlist cleared')
      return true
    } catch (err) {
      console.error('Error clearing wishlist:', err)
      error.value = err.message
      toast.error('Failed to clear wishlist')
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  // Move item to cart
  const moveToCart = async (itemId, quantity = 1) => {
    if (!isAuthenticated.value) {
      return false
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      await ensureValidToken()
      const response = await fetch(`${useRuntimeConfig().public.apiBase}/wishlist/move-to-cart/${itemId}`, {
        method: 'POST',
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity })
      })
      
      if (!response.ok) {
        throw new Error('Failed to move item to cart')
      }
      
      // Refresh wishlist
      await loadWishlist()
      
      toast.success('Item moved to cart')
      return true
    } catch (err) {
      console.error('Error moving to cart:', err)
      error.value = err.message
      toast.error('Failed to move item to cart')
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  // Initialize wishlist on auth state change
  watch(() => isAuthenticated.value, (newValue) => {
    if (newValue) {
      loadWishlist()
    } else {
      wishlistItems.value = []
    }
  }, { immediate: true })
  
  return {
    // State
    wishlistItems,
    isLoading,
    error,
    
    // Computed
    wishlistCount,
    wishlistTotal,
    
    // Methods
    loadWishlist,
    isInWishlist,
    getWishlistItem,
    addToWishlist,
    removeFromWishlist,
    toggleWishlist,
    clearWishlist,
    moveToCart
  }
}