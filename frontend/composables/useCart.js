import { ref, computed, readonly } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuth } from './useAuth'

// Create a global state for the cart
const cartItems = ref([])
const isLoading = ref(false)
const error = ref(null)

export const useCart = () => {
  const toast = useToast()
  const { isAuthenticated, user, accessToken } = useAuth()
  const config = useRuntimeConfig()
  const apiBase = config.public.apiBase

  // Computed properties
  const cartTotal = computed(() => {
    return cartItems.value.reduce((total, item) => {
      return total + (item.price * item.quantity)
    }, 0)
  })

  const cartCount = computed(() => {
    return cartItems.value.reduce((count, item) => {
      return count + item.quantity
    }, 0)
  })

  // Load cart from localStorage on client-side
  const initializeCart = async () => {
    isLoading.value = true
    error.value = null

    try {
      if (process.client) {
        // Try to load from localStorage first
        const storedCart = localStorage.getItem('cart')
        if (storedCart) {
          cartItems.value = JSON.parse(storedCart)
        }

        // If user is authenticated, fetch cart from API and merge with local cart
        if (isAuthenticated.value) {
          await syncWithServer()
        }
      }
    } catch (err) {
      console.error('Error initializing cart:', err)
      error.value = 'Failed to load your cart'
    } finally {
      isLoading.value = false
    }
  }

  // Sync cart with server (for authenticated users)
  const syncWithServer = async () => {
    if (!isAuthenticated.value) return

    try {
      // Get cart from server
      const response = await $fetch(`${apiBase}/cart`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        }
      })

      // If we have items in local storage but not on server, push them to server
      if (cartItems.value.length > 0 && (!response.items || response.items.length === 0)) {
        await $fetch(`${apiBase}/cart/sync`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          },
          body: {
            items: cartItems.value
          }
        })
      } else if (response.items && response.items.length > 0) {
        // Replace local cart with server cart
        cartItems.value = response.items
        saveToLocalStorage()
      }
    } catch (err) {
      console.error('Error syncing cart with server:', err)
      // Don't set error here to avoid disrupting the user experience
    }
  }

  // Save cart to localStorage
  const saveToLocalStorage = () => {
    if (process.client) {
      localStorage.setItem('cart', JSON.stringify(cartItems.value))
    }
  }

  // Add item to cart
  const addToCart = async (product, quantity = 1, variant = null) => {
    isLoading.value = true
    error.value = null

    try {
      // Check if product is already in cart
      const existingItemIndex = cartItems.value.findIndex(item => {
        if (variant) {
          return item.product.id === product.id && 
                 item.variant && 
                 item.variant.id === variant.id
        }
        return item.product.id === product.id && !item.variant
      })

      if (existingItemIndex !== -1) {
        // Update quantity if product is already in cart
        cartItems.value[existingItemIndex].quantity += quantity
      } else {
        // Add new item to cart
        cartItems.value.push({
          product: {
            id: product.id,
            name: product.name,
            main_image: product.main_image,
            slug: product.slug
          },
          variant: variant,
          quantity: quantity,
          price: variant ? variant.price : product.price
        })
      }

      // Save to localStorage
      saveToLocalStorage()

      // If user is authenticated, sync with server
      if (isAuthenticated.value) {
        await $fetch(`${apiBase}/cart`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          },
          body: {
            product_id: product.id,
            variant_id: variant?.id,
            quantity: quantity
          }
        })
      }

      toast.success('Item added to cart')
    } catch (err) {
      console.error('Error adding to cart:', err)
      error.value = 'Failed to add item to cart'
      toast.error('Failed to add item to cart')
    } finally {
      isLoading.value = false
    }
  }

  // Update cart item quantity
  const updateCartItemQuantity = async (itemIndex, quantity) => {
    isLoading.value = true
    error.value = null

    try {
      if (quantity <= 0) {
        // Remove item if quantity is 0 or negative
        removeFromCart(itemIndex)
        return
      }

      // Update quantity
      cartItems.value[itemIndex].quantity = quantity

      // Save to localStorage
      saveToLocalStorage()

      // If user is authenticated, sync with server
      if (isAuthenticated.value) {
        const item = cartItems.value[itemIndex]
        await $fetch(`${apiBase}/cart/update`, {
          method: 'PUT',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          },
          body: {
            product_id: item.product.id,
            variant_id: item.variant?.id,
            quantity: quantity
          }
        })
      }
    } catch (err) {
      console.error('Error updating cart item:', err)
      error.value = 'Failed to update cart item'
      toast.error('Failed to update cart item')
    } finally {
      isLoading.value = false
    }
  }

  // Remove item from cart
  const removeFromCart = async (itemIndex) => {
    isLoading.value = true
    error.value = null

    try {
      const item = cartItems.value[itemIndex]
      
      // Remove from local cart
      cartItems.value.splice(itemIndex, 1)

      // Save to localStorage
      saveToLocalStorage()

      // If user is authenticated, sync with server
      if (isAuthenticated.value) {
        await $fetch(`${apiBase}/cart/remove`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          },
          body: {
            product_id: item.product.id,
            variant_id: item.variant?.id
          }
        })
      }

      toast.success('Item removed from cart')
    } catch (err) {
      console.error('Error removing from cart:', err)
      error.value = 'Failed to remove item from cart'
      toast.error('Failed to remove item from cart')
    } finally {
      isLoading.value = false
    }
  }

  // Clear cart
  const clearCart = async () => {
    isLoading.value = true
    error.value = null

    try {
      // Clear local cart
      cartItems.value = []

      // Save to localStorage
      saveToLocalStorage()

      // If user is authenticated, sync with server
      if (isAuthenticated.value) {
        await $fetch(`${apiBase}/cart/clear`, {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          }
        })
      }
    } catch (err) {
      console.error('Error clearing cart:', err)
      error.value = 'Failed to clear cart'
      toast.error('Failed to clear cart')
    } finally {
      isLoading.value = false
    }
  }

  // Initialize cart on client-side
  if (process.client) {
    initializeCart()

    // Watch for authentication changes
    watch(isAuthenticated, (newValue) => {
      if (newValue) {
        syncWithServer()
      }
    })
  }

  return {
    cartItems: readonly(cartItems),
    cartTotal,
    cartCount,
    isLoading: readonly(isLoading),
    error: readonly(error),
    addToCart,
    updateCartItemQuantity,
    removeFromCart,
    clearCart,
    initializeCart
  }
}