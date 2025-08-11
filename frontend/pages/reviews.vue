<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">My Reviews</h1>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Empty state -->
    <div v-else-if="userReviews.length === 0" class="text-center py-12">
      <div class="text-5xl mb-4">📝</div>
      <h3 class="text-xl font-semibold mb-2">You haven't written any reviews yet</h3>
      <p class="text-gray-600 mb-6">Share your thoughts on products you've purchased to help other shoppers</p>
      <NuxtLink to="/products" class="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary-dark transition">
        Browse Products
      </NuxtLink>
    </div>

    <!-- Reviews list -->
    <div v-else>
      <div class="grid grid-cols-1 gap-6">
        <div v-for="review in userReviews" :key="review.id" class="border rounded-lg p-6 shadow-sm hover:shadow-md transition">
          <div class="flex justify-between items-start mb-4">
            <div>
              <div class="flex items-center mb-2">
                <div class="flex">
                  <span v-for="i in 5" :key="i" class="text-xl">
                    <span v-if="i <= review.rating" class="text-yellow-400">★</span>
                    <span v-else class="text-gray-300">★</span>
                  </span>
                </div>
                <span class="ml-2 text-sm text-gray-600">
                  {{ new Date(review.created_at).toLocaleDateString() }}
                </span>
              </div>
              <h3 class="text-lg font-semibold">{{ review.title || 'Review' }}</h3>
            </div>
            <div class="flex space-x-2">
              <button @click="editReview(review)" class="text-blue-600 hover:text-blue-800">
                <span class="sr-only">Edit</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button @click="confirmDeleteReview(review)" class="text-red-600 hover:text-red-800">
                <span class="sr-only">Delete</span>
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>

          <p class="text-gray-700 mb-4">{{ review.comment }}</p>

          <!-- Review images -->
          <div v-if="review.images && review.images.length > 0" class="flex space-x-2 mb-4 overflow-x-auto pb-2">
            <div v-for="image in review.images" :key="image.id" class="flex-shrink-0">
              <img :src="image.image_url" :alt="image.alt_text || 'Review image'" class="h-20 w-20 object-cover rounded-md">
            </div>
          </div>

          <!-- Product info -->
          <div v-if="review.product" class="flex items-center mt-4 pt-4 border-t">
            <img 
              :src="review.product.main_image" 
              :alt="review.product.name" 
              class="h-16 w-16 object-cover rounded-md"
            >
            <div class="ml-4">
              <NuxtLink :to="`/products/${review.product.id}`" class="text-primary hover:underline font-medium">
                {{ review.product.name }}
              </NuxtLink>
              <div v-if="review.is_verified_purchase" class="text-xs text-green-600 mt-1">
                Verified Purchase
              </div>
            </div>
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
    </div>

    <!-- Edit Review Modal -->
    <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-lg mx-4">
        <h2 class="text-xl font-bold mb-4">Edit Review</h2>
        
        <div class="mb-4">
          <label class="block text-gray-700 mb-2">Rating</label>
          <div class="flex">
            <button 
              v-for="i in 5" 
              :key="i"
              @click="editedReview.rating = i"
              class="text-2xl focus:outline-none"
              :class="i <= editedReview.rating ? 'text-yellow-400' : 'text-gray-300'"
            >
              ★
            </button>
          </div>
        </div>
        
        <div class="mb-4">
          <label for="title" class="block text-gray-700 mb-2">Title</label>
          <input 
            id="title"
            v-model="editedReview.title"
            type="text"
            class="w-full px-3 py-2 border rounded-md"
            placeholder="Review title"
          >
        </div>
        
        <div class="mb-4">
          <label for="comment" class="block text-gray-700 mb-2">Comment</label>
          <textarea 
            id="comment"
            v-model="editedReview.comment"
            rows="4"
            class="w-full px-3 py-2 border rounded-md"
            placeholder="Your review"
          ></textarea>
        </div>
        
        <!-- Image upload would go here -->
        
        <div class="flex justify-end space-x-3 mt-6">
          <button 
            @click="showEditModal = false"
            class="px-4 py-2 border rounded-md hover:bg-gray-100"
          >
            Cancel
          </button>
          <button 
            @click="saveReview"
            class="px-4 py-2 bg-primary text-white rounded-md hover:bg-primary-dark"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting">Saving...</span>
            <span v-else>Save Changes</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
        <h2 class="text-xl font-bold mb-4">Delete Review</h2>
        <p class="mb-6">Are you sure you want to delete this review? This action cannot be undone.</p>
        
        <div class="flex justify-end space-x-3">
          <button 
            @click="showDeleteModal = false"
            class="px-4 py-2 border rounded-md hover:bg-gray-100"
          >
            Cancel
          </button>
          <button 
            @click="deleteReviewConfirmed"
            class="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting">Deleting...</span>
            <span v-else>Delete</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useReviews } from '~/composables/useReviews'
import { useToast } from 'vue-toastification'

const toast = useToast()
const { 
  userReviews, 
  pagination, 
  isLoading, 
  error, 
  getUserReviews,
  updateReview,
  deleteReview
} = useReviews()

// Modal state
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const isSubmitting = ref(false)
const editedReview = ref({})
const reviewToDelete = ref(null)

onMounted(async () => {
  await getUserReviews()
})

const changePage = async (page) => {
  await getUserReviews({ page })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const editReview = (review) => {
  editedReview.value = { ...review }
  showEditModal.value = true
}

const saveReview = async () => {
  if (!editedReview.value.rating) {
    toast.error('Please select a rating')
    return
  }
  
  isSubmitting.value = true
  
  try {
    await updateReview(editedReview.value.id, {
      rating: editedReview.value.rating,
      title: editedReview.value.title,
      comment: editedReview.value.comment,
      // images would be handled here
    })
    
    showEditModal.value = false
  } catch (err) {
    console.error('Error saving review:', err)
  } finally {
    isSubmitting.value = false
  }
}

const confirmDeleteReview = (review) => {
  reviewToDelete.value = review
  showDeleteModal.value = true
}

const deleteReviewConfirmed = async () => {
  if (!reviewToDelete.value) return
  
  isSubmitting.value = true
  
  try {
    const success = await deleteReview(reviewToDelete.value.id)
    if (success) {
      showDeleteModal.value = false
      reviewToDelete.value = null
    }
  } catch (err) {
    console.error('Error deleting review:', err)
  } finally {
    isSubmitting.value = false
  }
}
</script>