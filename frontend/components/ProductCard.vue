<template>
  <div class="product-card group">
    <!-- Product Image -->
    <div class="relative aspect-square overflow-hidden rounded-t-xl">
      <img 
        :src="product.main_image || product.images?.[0]?.image_url || '/images/placeholder.jpg'"
        :alt="product.name"
        class="product-image w-full h-full object-cover"
        loading="lazy"
      >
      
      <!-- Product Overlay -->
      <div class="product-overlay">
        <div class="flex space-x-2">
          <button 
            @click="addToWishlist"
            class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-md hover:scale-110 transition-transform"
            :class="{ 'text-rose-gold': isInWishlist, 'text-gray-600': !isInWishlist }"
          >
            <Icon 
              :name="isInWishlist ? 'heroicons:heart' : 'heroicons:heart'" 
              class="w-5 h-5"
              :class="{ 'fill-current': isInWishlist }"
            />
          </button>
          
          <button 
            @click="quickView"
            class="w-10 h-10 bg-white rounded-full flex items-center justify-center shadow-md hover:scale-110 transition-transform text-gray-600"
          >
            <Icon name="heroicons:eye" class="w-5 h-5" />
          </button>
        </div>
      </div>

      <!-- Product Actions -->
      <div class="product-actions">
        <button 
          @click="addToWishlist"
          class="w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md hover:scale-110 transition-transform"
          :class="{ 'text-rose-gold': isInWishlist, 'text-gray-600': !isInWishlist }"
        >
          <Icon 
            :name="isInWishlist ? 'heroicons:heart' : 'heroicons:heart'" 
            class="w-4 h-4"
            :class="{ 'fill-current': isInWishlist }"
          />
        </button>
      </div>

      <!-- Discount Badge -->
      <div 
        v-if="product.discount_percentage > 0"
        class="absolute top-2 left-2 bg-red-500 text-white text-xs px-2 py-1 rounded-full font-medium"
      >
        -{{ product.discount_percentage }}%
      </div>

      <!-- Out of Stock Badge -->
      <div 
        v-if="!product.is_in_stock"
        class="absolute top-2 right-2 bg-gray-500 text-white text-xs px-2 py-1 rounded-full font-medium"
      >
        Out of Stock
      </div>
    </div>

    <!-- Product Info -->
    <div class="p-4">
      <!-- Category -->
      <p class="text-xs text-gray-500 mb-1">{{ product.category?.name || 'Jewelry' }}</p>
      
      <!-- Product Name -->
      <h3 class="font-display text-lg text-gray-900 mb-2 line-clamp-2">
        {{ product.name }}
      </h3>
      
      <!-- Product Details -->
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center space-x-2">
          <!-- Rating -->
          <div class="flex">
            <Icon 
              v-for="star in 5" 
              :key="star"
              :name="star <= product.average_rating ? 'heroicons:star' : 'heroicons:star'"
              class="w-4 h-4"
              :class="star <= product.average_rating ? 'text-yellow-400 fill-current' : 'text-gray-300'"
            />
          </div>
          <span class="text-xs text-gray-500">({{ product.review_count || 0 }})</span>
        </div>
        
        <!-- Material -->
        <span v-if="product.material" class="text-xs text-gray-500">
          {{ product.material }}
        </span>
      </div>
      
      <!-- Price -->
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-2">
          <span class="text-xl font-display text-gray-900">
            ₹{{ formatPrice(product.price) }}
          </span>
          <span 
            v-if="product.compare_at_price && product.compare_at_price > product.price"
            class="text-sm text-gray-500 line-through"
          >
            ₹{{ formatPrice(product.compare_at_price) }}
          </span>
        </div>
        
        <!-- Weight -->
        <span v-if="product.weight" class="text-xs text-gray-500">
          {{ product.weight }}g
        </span>
      </div>
      
      <!-- Add to Cart Button -->
      <button 
        @click="addToCart"
        :disabled="!product.is_in_stock"
        class="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <span v-if="product.is_in_stock">Add to Cart</span>
        <span v-else>Out of Stock</span>
      </button>
    </div>
  </div>
</template>

<script setup>
// Props
const props = defineProps({
  product: {
    type: Object,
    required: true
  }
})

// Emits
const emit = defineEmits(['add-to-cart', 'add-to-wishlist', 'quick-view'])

// Import composables
import { useWishlist } from '~/composables/useWishlist'

// Use wishlist composable
const { isInWishlist, toggleWishlist } = useWishlist()

// Methods
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN').format(price)
}

const addToCart = () => {
  if (props.product.is_in_stock) {
    emit('add-to-cart', props.product)
  }
}

const addToWishlist = async () => {
  await toggleWishlist(props.product)
  emit('add-to-wishlist', props.product)
}

const quickView = () => {
  emit('quick-view', props.product)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Custom hover effects */
.product-card:hover .product-overlay {
  opacity: 1;
}

.product-card:hover .product-actions {
  opacity: 1;
}

/* Loading skeleton */
.product-card.loading {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: .5;
  }
}
</style>