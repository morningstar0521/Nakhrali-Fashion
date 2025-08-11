<template>
  <div class="product-reviews">
    <h2 class="text-2xl font-bold mb-6">Customer Reviews</h2>
    
    <!-- Review Summary -->
    <div class="review-summary bg-gray-50 p-6 rounded-lg mb-8">
      <div class="flex flex-col md:flex-row">
        <!-- Rating Overview -->
        <div class="md:w-1/3 mb-6 md:mb-0">
          <div class="flex items-baseline">
            <span class="text-5xl font-bold">{{ averageRating }}</span>
            <span class="text-gray-500 ml-2">out of 5</span>
          </div>
          <div class="flex mt-2">
            <span v-for="i in 5" :key="i" class="text-xl">
              <span v-if="i <= Math.round(averageRating)" class="text-yellow-400">★</span>
              <span v-else class="text-gray-300">★</span>
            </span>
          </div>
          <div class="text-sm text-gray-500 mt-2">{{ totalReviews }} ratings</div>
        </div>
        
        <!-- Rating Distribution -->
        <div class="md:w-2/3">
          <div v-for="i in [5, 4, 3, 2, 1]" :key="i" class="flex items-center mb-2">
            <div class="flex items-center w-16">
              <span>{{ i }}</span>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-400 ml-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <div class="w-full">
              <div class="bg-gray-200 rounded-full h-2 w-full">
                <div 
                  class="bg-yellow-400 h-2 rounded-full" 
                  :style="{ width: calculatePercentage(ratingDistribution[i]) + '%' }"
                ></div>
              </div>
            </div>
            <div class="w-16 text-right text-sm text-gray-500">
              {{ ratingDistribution[i] }}
            </div>
          </div>
        </div>
      </div>
      
      <!-- Write Review Button -->
      <div class="mt-6">
        <button 
          v-if="isAuthenticated && canReview" 
          @click="showReviewForm = true"
          class="bg-primary text-white px-4 py-2 rounded-md hover:bg-primary-dark transition"
        >
          Write a Review
        </button>
        <div v-else-if="isAuthenticated && !canReview" class="text-sm text-gray-500">
          You've already reviewed this product
        </div>
        <div v-else class="text-sm text-gray-500">
          <NuxtLink to="/login" class="text-primary hover:underline">Sign in</NuxtLink> to write a review
        </div>
      </div>
    </div>
    
    <!-- Review Filters -->
    <div class="review-filters flex flex-wrap gap-2 mb-6">
      <button 
        @click="setRatingFilter(0)"
        :class="[
          'px-3 py-1 rounded-full text-sm',
          ratingFilter === 0 
            ? 'bg-primary text-white' 
            : 'bg-gray-100 hover:bg-gray-200'
        ]"
      >
        All Reviews
      </button>
      <button 
        v-for="i in 5" 
        :key="i"
        @click="setRatingFilter(i)"
        :class="[
          'px-3 py-1 rounded-full text-sm flex items-center',
          ratingFilter === i 
            ? 'bg-primary text-white' 
            : 'bg-gray-100 hover:bg-gray-200'
        ]"
      >
        {{ i }} <span class="ml-1">★</span>
      </button>
      <button 
        @click="toggleVerifiedFilter"
        :class="[
          'px-3 py-1 rounded-full text-sm',
          verifiedOnly 
            ? 'bg-primary text-white' 
            : 'bg-gray-100 hover:bg-gray-200'
        ]"
      >
        Verified Purchases
      </button>
      <button 
        @click="toggleImagesFilter"
        :class="[
          'px-3 py-1 rounded-full text-sm',
          hasImages 
            ? 'bg-primary text-white' 
            : 'bg-gray-100 hover:bg-gray-200'
        ]"
      >
        With Images
      </button>
    </div>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>
    
    <!-- No Reviews -->
    <div v-else-if="productReviews.length === 0" class="text-center py-12 bg-gray-50 rounded-lg">
      <div class="text-5xl mb-4">📝</div>
      <h3 class="text-xl font-semibold mb-2">No reviews yet</h3>
      <p class="text-gray-600">
        Be the first to review this product
      </p>
    </div>
    
    <!-- Reviews List -->
    <div v-else class="space-y-8">
      <div 
        v-for="review in productReviews" 
        :key="review.id"
        class="review border-b pb-8"
      >
        <div class="flex justify-between">
          <div class="flex items-center">
            <div class="w-10 h-10 bg-gray-200 rounded-full flex items-center justify-center text-gray-600 mr-3">
              {{ review.user?.name?.charAt(0) || 'U' }}
            </div>
            <div>
              <div class="font-medium">{{ review.user?.name || 'Anonymous' }}</div>
              <div class="text-sm text-gray-500">
                {{ new Date(review.created_at).toLocaleDateString() }}
                <span v-if="review.is_verified_purchase" class="ml-2 text-green-600 text-xs">
                  Verified Purchase
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-3">
          <div class="flex mb-2">
            <span v-for="i in 5" :key="i" class="text-lg">
              <span v-if="i <= review.rating" class="text-yellow-400">★</span>
              <span v-else class="text-gray-300">★</span>
            </span>
          </div>
          <h4 class="font-semibold text-lg mb-2">{{ review.title || 'Review' }}</h4>
          <p class="text-gray-700">{{ review.comment }}</p>
        </div>
        
        <!-- Review Images -->
        <div v-if="review.images && review.images.length > 0" class="mt-4 flex space-x-2 overflow-x-auto">
          <div 
            v-for="image in review.images" 
            :key="image.id"
            class="flex-shrink-0"
          >
            <img 
              :src="image.image_url" 
              :alt="image.alt_text || 'Review image'"
              class="h-24 w-24 object-cover rounded-md cursor-pointer"
              @click="openImageModal(image.image_url)"
            >
          </div>
        </div>
        
        <!-- Helpful Button -->
        <div class="mt-4 flex items-center">
          <button 
            @click="markHelpful(review.id)"
            class="text-sm text-gray-500 hover:text-gray-700 flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5" />
            </svg>
            Helpful ({{ review.is_helpful || 0 }})
          </button>
        </div>
      </div>
    </div>
    
    <!-- Pagination -->
    <div v-if="pagination.total_pages > 1" class="flex justify-center mt-8">
      <button 
        v-for="page in pagination.total_pages" 
        :key="page"
        @click="changePage(page)"
        :class="[
          'mx-1 px-3 py-1 rounded',
          page === pagination.page 
            ? 'bg-primary text-white' 
            : 'bg-gray-200 hover:bg-gray-300'
        ]"
      >
        {{ page }}
      </button>
    </div>
    
    <!-- Review Form Modal -->
    <div v-if="showReviewForm" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-lg mx-4">
        <h2 class="text-xl font-bold mb-4">Write a Review</h2>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Rating</label>
          <div class="flex">
            <button 
              v-for="i in 5" 
              :key="i"
              @click="newReview.rating = i"
              class="text-2xl focus:outline-none"
              :class="i <= newReview.rating ? 'text-yellow-400' : 'text-gray-300'"
            >
              ★
            </button>
          </div>
        </div>
        
        <div class="mb-4">
          <label for="title" class="block text-gray-700 mb-2">Title</label>
          <input 
            id="title"
            v-model="newReview.title"
            type="text"
            class="w-full px-3 py-2 border rounded-md"
            placeholder="Review title"
          >
        </div>
        
        <div class="mb-4">
          <label for="comment" class="block text-gray-700 mb-2">Comment</label>
          <textarea 
            id="comment"
            v-model="newReview.comment"
            rows="4"
            class="w-full px-3 py-2 border rounded-md"
            placeholder="Your review"
          ></textarea>
        </div>
        
        <!-- Image upload would go here -->
        
        <div class="flex justify-end space-x-3 mt-6">
          <button 
            @click="showReviewForm = false"
            class="px-4 py-2 border rounded-md hover:bg-gray-100"
          >
            Cancel
          </button>
          <button 
            @click="submitReview"
            class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting">Submitting...</span>
            <span v-else>Submit Review</span>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Image Modal -->
    <div v-if="imageModal.show" class="fixed inset-0 bg-black bg-opacity-90 flex items-center justify-center z-50">
      <button @click="imageModal.show = false" class="absolute top-4 right-4 text-white">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <img :src="imageModal.url" class="max-h-[80vh] max-w-[90vw] object-contain">
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useReviews } from '~/composables/useReviews'
import { useAuth } from '~/composables/useAuth'
import { useToast } from 'vue-toastification'

const props = defineProps({
  productId: {
    type: String,
    required: true
  }
})

const toast = useToast()
const { isAuthenticated } = useAuth()
const { 
  productReviews, 
  reviewStats, 
  pagination, 
  isLoading, 
  error,
  averageRating,
  totalReviews,
  ratingDistribution,
  getProductReviews,
  addReview,
  markReviewHelpful,
  canReviewProduct
} = useReviews()

// Filters
const ratingFilter = ref(0)
const verifiedOnly = ref(false)
const hasImages = ref(false)

// Review form
const showReviewForm = ref(false)
const isSubmitting = ref(false)
const canReview = ref(false)
const newReview = ref({
  product_id: props.productId,
  rating: 5,
  title: '',
  comment: '',
  images: []
})

// Image modal
const imageModal = ref({
  show: false,
  url: ''
})

onMounted(async () => {
  await loadReviews()
  checkCanReview()
})

watch([ratingFilter, verifiedOnly, hasImages], () => {
  loadReviews()
})

const loadReviews = async () => {
  await getProductReviews(props.productId, {
    rating: ratingFilter.value || undefined,
    verifiedOnly: verifiedOnly.value,
    hasImages: hasImages.value,
    page: pagination.value.page
  })
}

const checkCanReview = async () => {
  if (isAuthenticated.value) {
    canReview.value = await canReviewProduct(props.productId)
  }
}

const setRatingFilter = (rating) => {
  ratingFilter.value = rating === ratingFilter.value ? 0 : rating
}

const toggleVerifiedFilter = () => {
  verifiedOnly.value = !verifiedOnly.value
}

const toggleImagesFilter = () => {
  hasImages.value = !hasImages.value
}

const changePage = async (page) => {
  pagination.value.page = page
  await loadReviews()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const submitReview = async () => {
  if (!newReview.value.rating) {
    toast.error('Please select a rating')
    return
  }
  
  isSubmitting.value = true
  
  try {
    await addReview(newReview.value)
    showReviewForm.value = false
    newReview.value = {
      product_id: props.productId,
      rating: 5,
      title: '',
      comment: '',
      images: []
    }
    canReview.value = false
  } catch (err) {
    console.error('Error submitting review:', err)
  } finally {
    isSubmitting.value = false
  }
}

const markHelpful = async (reviewId) => {
  await markReviewHelpful(reviewId)
}

const openImageModal = (url) => {
  imageModal.value.url = url
  imageModal.value.show = true
}

const calculatePercentage = (count) => {
  if (!totalReviews.value || totalReviews.value === 0) return 0
  return Math.round((count / totalReviews.value) * 100)
}
</script>