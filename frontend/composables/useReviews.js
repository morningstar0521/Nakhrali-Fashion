import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useAuth } from './useAuth'
import { useRuntimeConfig } from '#app'

export function useReviews() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseURL || '/api'
  const toast = useToast()
  const { isAuthenticated, getAuthToken } = useAuth()

  // State
  const productReviews = ref([])
  const userReviews = ref([])
  const reviewStats = ref({
    average_rating: 0,
    total_reviews: 0,
    rating_distribution: {
      '5': 0, '4': 0, '3': 0, '2': 0, '1': 0
    }
  })
  const pagination = ref({
    page: 1,
    per_page: 10,
    total: 0,
    total_pages: 0,
    has_next: false,
    has_prev: false
  })
  const isLoading = ref(false)
  const error = ref(null)

  // Computed
  const averageRating = computed(() => reviewStats.value.average_rating)
  const totalReviews = computed(() => reviewStats.value.total_reviews)
  const ratingDistribution = computed(() => reviewStats.value.rating_distribution)

  // Get reviews for a product
  const getProductReviews = async (productId, options = {}) => {
    if (!productId) return
    
    isLoading.value = true
    error.value = null
    
    try {
      // Build query parameters
      const params = new URLSearchParams()
      if (options.page) params.append('page', options.page)
      if (options.perPage) params.append('per_page', options.perPage)
      if (options.rating) params.append('rating', options.rating)
      if (options.verifiedOnly) params.append('verified_only', options.verifiedOnly)
      if (options.hasImages) params.append('has_images', options.hasImages)
      
      const queryString = params.toString() ? `?${params.toString()}` : ''
      const response = await fetch(`${baseURL}/reviews/product/${productId}${queryString}`)
      
      if (!response.ok) {
        throw new Error('Failed to fetch reviews')
      }
      
      const data = await response.json()
      productReviews.value = data.reviews
      reviewStats.value = data.rating_stats
      pagination.value = data.pagination
      
      return data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching product reviews:', err)
      toast.error('Failed to load reviews')
    } finally {
      isLoading.value = false
    }
  }

  // Get reviews by current user
  const getUserReviews = async (options = {}) => {
    if (!isAuthenticated.value) {
      toast.error('You must be logged in to view your reviews')
      return
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      // Build query parameters
      const params = new URLSearchParams()
      if (options.page) params.append('page', options.page)
      if (options.perPage) params.append('per_page', options.perPage)
      
      const queryString = params.toString() ? `?${params.toString()}` : ''
      const response = await fetch(`${baseURL}/reviews/user${queryString}`, {
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to fetch your reviews')
      }
      
      const data = await response.json()
      userReviews.value = data.reviews
      pagination.value = data.pagination
      
      return data
    } catch (err) {
      error.value = err.message
      console.error('Error fetching user reviews:', err)
      toast.error('Failed to load your reviews')
    } finally {
      isLoading.value = false
    }
  }

  // Add a new review
  const addReview = async (reviewData) => {
    if (!isAuthenticated.value) {
      toast.error('You must be logged in to add a review')
      return
    }
    
    if (!reviewData.product_id || !reviewData.rating) {
      toast.error('Product ID and rating are required')
      return
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${baseURL}/reviews/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify(reviewData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to add review')
      }
      
      const data = await response.json()
      toast.success('Review added successfully')
      
      // Refresh product reviews if we're on the product page
      if (reviewData.product_id) {
        await getProductReviews(reviewData.product_id)
      }
      
      return data.review
    } catch (err) {
      error.value = err.message
      console.error('Error adding review:', err)
      toast.error(err.message || 'Failed to add review')
    } finally {
      isLoading.value = false
    }
  }

  // Update an existing review
  const updateReview = async (reviewId, reviewData) => {
    if (!isAuthenticated.value) {
      toast.error('You must be logged in to update a review')
      return
    }
    
    if (!reviewId) {
      toast.error('Review ID is required')
      return
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${baseURL}/reviews/${reviewId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify(reviewData)
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to update review')
      }
      
      const data = await response.json()
      toast.success('Review updated successfully')
      
      // Refresh user reviews
      await getUserReviews()
      
      // Refresh product reviews if we're on the product page
      if (reviewData.product_id) {
        await getProductReviews(reviewData.product_id)
      }
      
      return data.review
    } catch (err) {
      error.value = err.message
      console.error('Error updating review:', err)
      toast.error(err.message || 'Failed to update review')
    } finally {
      isLoading.value = false
    }
  }

  // Delete a review
  const deleteReview = async (reviewId, productId = null) => {
    if (!isAuthenticated.value) {
      toast.error('You must be logged in to delete a review')
      return
    }
    
    if (!reviewId) {
      toast.error('Review ID is required')
      return
    }
    
    isLoading.value = true
    error.value = null
    
    try {
      const response = await fetch(`${baseURL}/reviews/${reviewId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      })
      
      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to delete review')
      }
      
      toast.success('Review deleted successfully')
      
      // Refresh user reviews
      await getUserReviews()
      
      // Refresh product reviews if we're on the product page
      if (productId) {
        await getProductReviews(productId)
      }
      
      return true
    } catch (err) {
      error.value = err.message
      console.error('Error deleting review:', err)
      toast.error(err.message || 'Failed to delete review')
      return false
    } finally {
      isLoading.value = false
    }
  }

  // Mark a review as helpful
  const markReviewHelpful = async (reviewId) => {
    if (!reviewId) return
    
    try {
      const headers = {}
      if (isAuthenticated.value) {
        headers['Authorization'] = `Bearer ${getAuthToken()}`
      }
      
      const response = await fetch(`${baseURL}/reviews/${reviewId}/helpful`, {
        method: 'POST',
        headers
      })
      
      if (!response.ok) {
        throw new Error('Failed to mark review as helpful')
      }
      
      const data = await response.json()
      
      // Update the helpful count in the local reviews array
      const reviewIndex = productReviews.value.findIndex(r => r.id === reviewId)
      if (reviewIndex !== -1) {
        productReviews.value[reviewIndex].is_helpful = data.helpful_count
      }
      
      return data.helpful_count
    } catch (err) {
      console.error('Error marking review as helpful:', err)
      toast.error('Failed to mark review as helpful')
    }
  }

  // Check if user can review a product
  const canReviewProduct = async (productId) => {
    if (!isAuthenticated.value || !productId) return false
    
    try {
      // First check if user has already reviewed this product
      const response = await fetch(`${baseURL}/reviews/user`, {
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      })
      
      if (!response.ok) {
        throw new Error('Failed to check review eligibility')
      }
      
      const data = await response.json()
      const hasReviewed = data.reviews.some(review => review.product.id === productId)
      
      if (hasReviewed) {
        return false
      }
      
      // TODO: Check if user has purchased the product
      // This would require an endpoint to check purchase history
      // For now, we'll assume they can review if they haven't already
      
      return true
    } catch (err) {
      console.error('Error checking review eligibility:', err)
      return false
    }
  }

  return {
    // State
    productReviews,
    userReviews,
    reviewStats,
    pagination,
    isLoading,
    error,
    
    // Computed
    averageRating,
    totalReviews,
    ratingDistribution,
    
    // Methods
    getProductReviews,
    getUserReviews,
    addReview,
    updateReview,
    deleteReview,
    markReviewHelpful,
    canReviewProduct
  }
}