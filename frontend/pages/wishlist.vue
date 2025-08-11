<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-display font-bold mb-8">My Wishlist</h1>
    
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-rose-gold"></div>
    </div>
    
    <!-- Empty Wishlist -->
    <div v-else-if="!wishlistItems.length" class="text-center py-12">
      <div class="mb-6">
        <Icon name="heroicons:heart" class="w-16 h-16 mx-auto text-gray-300" />
      </div>
      <h2 class="text-2xl font-display font-medium mb-4">Your wishlist is empty</h2>
      <p class="text-gray-500 mb-6">Add items to your wishlist to save them for later.</p>
      <NuxtLink to="/products" class="btn-primary inline-block">
        Browse Products
      </NuxtLink>
    </div>
    
    <!-- Wishlist Items -->
    <div v-else>
      <!-- Wishlist Actions -->
      <div class="flex justify-between items-center mb-6">
        <div>
          <span class="text-gray-500">{{ wishlistCount }} items</span>
        </div>
        <button 
          @click="clearWishlist"
          class="text-sm text-rose-gold hover:underline"
        >
          Clear Wishlist
        </button>
      </div>
      
      <!-- Wishlist Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div 
          v-for="item in wishlistItems" 
          :key="item.id"
          class="border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
        >
          <!-- Product Image -->
          <div class="relative aspect-square overflow-hidden">
            <img 
              :src="item.product?.main_image || item.product?.images?.[0]?.image_url || '/images/placeholder.jpg'"
              :alt="item.product?.name"
              class="w-full h-full object-cover"
              loading="lazy"
            >
            
            <!-- Remove Button -->
            <button 
              @click="removeFromWishlist(item.id)"
              class="absolute top-2 right-2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md hover:bg-rose-gold hover:text-white transition-colors"
            >
              <Icon name="heroicons:x-mark" class="w-4 h-4" />
            </button>
          </div>
          
          <!-- Product Info -->
          <div class="p-4">
            <!-- Category -->
            <p class="text-xs text-gray-500 mb-1">{{ item.product?.category?.name || 'Jewelry' }}</p>
            
            <!-- Product Name -->
            <h3 class="font-display text-lg text-gray-900 mb-2 line-clamp-2">
              {{ item.product?.name }}
            </h3>
            
            <!-- Price -->
            <div class="flex items-center justify-between mb-4">
              <div>
                <span class="font-medium text-lg">₹{{ formatPrice(item.product?.price) }}</span>
                <span 
                  v-if="item.product?.compare_at_price && item.product?.compare_at_price > item.product?.price"
                  class="text-gray-400 line-through ml-2"
                >
                  ₹{{ formatPrice(item.product?.compare_at_price) }}
                </span>
              </div>
              
              <!-- Priority Badge -->
              <span 
                class="text-xs px-2 py-1 rounded-full"
                :class="{
                  'bg-red-100 text-red-800': item.priority === 'high',
                  'bg-yellow-100 text-yellow-800': item.priority === 'medium',
                  'bg-blue-100 text-blue-800': item.priority === 'low'
                }"
              >
                {{ item.priority }}
              </span>
            </div>
            
            <!-- Actions -->
            <div class="flex space-x-2">
              <button 
                @click="moveToCart(item.id)"
                class="flex-1 btn-primary text-sm py-2"
                :disabled="!item.product?.is_in_stock"
              >
                <Icon name="heroicons:shopping-cart" class="w-4 h-4 mr-1" />
                Add to Cart
              </button>
              <NuxtLink 
                :to="`/products/${item.product?.id}`"
                class="w-10 h-10 border border-gray-300 rounded-lg flex items-center justify-center hover:border-rose-gold transition-colors"
              >
                <Icon name="heroicons:eye" class="w-4 h-4" />
              </NuxtLink>
            </div>
            
            <!-- Notes -->
            <div v-if="item.notes" class="mt-4 pt-4 border-t border-gray-100">
              <p class="text-sm text-gray-500 italic">{{ item.notes }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useWishlist } from '~/composables/useWishlist'

// Define meta
definePageMeta({
  middleware: ['auth'],
  layout: 'default'
})

// Use wishlist composable
const {
  wishlistItems,
  isLoading,
  wishlistCount,
  removeFromWishlist,
  clearWishlist,
  moveToCart
} = useWishlist()

// Format price
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN').format(price || 0)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.btn-primary {
  @apply bg-rose-gold text-white rounded-lg px-4 py-2 font-medium hover:bg-rose-gold-dark transition-colors disabled:opacity-50 disabled:cursor-not-allowed;
}
</style>