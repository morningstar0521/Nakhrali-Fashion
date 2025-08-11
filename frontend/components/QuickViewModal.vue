<template>
  <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto">
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200">
        <h2 class="text-2xl font-display text-gray-900">Quick View</h2>
        <button 
          @click="$emit('close')"
          class="p-2 text-gray-400 hover:text-gray-600 transition-colors"
        >
          <Icon name="heroicons:x-mark" class="w-6 h-6" />
        </button>
      </div>

      <!-- Content -->
      <div class="p-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Product Images -->
          <div>
            <div class="relative aspect-square rounded-xl overflow-hidden mb-4">
              <img 
                :src="currentImage || product.main_image || '/images/placeholder.jpg'"
                :alt="product.name"
                class="w-full h-full object-cover"
              >
              
              <!-- Image Navigation -->
              <button 
                v-if="product.images && product.images.length > 1"
                @click="previousImage"
                class="absolute left-2 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md"
              >
                <Icon name="heroicons:chevron-left" class="w-4 h-4" />
              </button>
              
              <button 
                v-if="product.images && product.images.length > 1"
                @click="nextImage"
                class="absolute right-2 top-1/2 transform -translate-y-1/2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md"
              >
                <Icon name="heroicons:chevron-right" class="w-4 h-4" />
              </button>
            </div>

            <!-- Thumbnail Images -->
            <div v-if="product.images && product.images.length > 1" class="flex space-x-2">
              <button 
                v-for="(image, index) in product.images" 
                :key="index"
                @click="currentImageIndex = index"
                class="w-16 h-16 rounded-lg overflow-hidden border-2 transition-colors"
                :class="currentImageIndex === index ? 'border-rose-gold' : 'border-gray-200'"
              >
                <img 
                  :src="image.image_url" 
                  :alt="image.alt_text"
                  class="w-full h-full object-cover"
                >
              </button>
            </div>
          </div>

          <!-- Product Details -->
          <div>
            <!-- Category -->
            <p class="text-sm text-gray-500 mb-2">{{ product.category?.name || 'Jewelry' }}</p>
            
            <!-- Product Name -->
            <h1 class="text-2xl font-display text-gray-900 mb-4">{{ product.name }}</h1>
            
            <!-- Rating -->
            <div class="flex items-center space-x-2 mb-4">
              <div class="flex">
                <Icon 
                  v-for="star in 5" 
                  :key="star"
                  :name="star <= product.average_rating ? 'heroicons:star' : 'heroicons:star'"
                  class="w-5 h-5"
                  :class="star <= product.average_rating ? 'text-yellow-400 fill-current' : 'text-gray-300'"
                />
              </div>
              <span class="text-sm text-gray-500">
                {{ product.average_rating || 0 }} ({{ product.review_count || 0 }} reviews)
              </span>
            </div>
            
            <!-- Price -->
            <div class="flex items-center space-x-3 mb-6">
              <span class="text-3xl font-display text-gray-900">
                ₹{{ formatPrice(product.price) }}
              </span>
              <span 
                v-if="product.compare_at_price && product.compare_at_price > product.price"
                class="text-lg text-gray-500 line-through"
              >
                ₹{{ formatPrice(product.compare_at_price) }}
              </span>
              <span 
                v-if="product.discount_percentage > 0"
                class="bg-red-500 text-white text-sm px-2 py-1 rounded-full"
              >
                -{{ product.discount_percentage }}%
              </span>
            </div>
            
            <!-- Product Details -->
            <div class="space-y-3 mb-6">
              <div v-if="product.material" class="flex justify-between">
                <span class="text-gray-600">Material:</span>
                <span class="font-medium">{{ product.material }}</span>
              </div>
              <div v-if="product.weight" class="flex justify-between">
                <span class="text-gray-600">Weight:</span>
                <span class="font-medium">{{ product.weight }}g</span>
              </div>
              <div v-if="product.purity" class="flex justify-between">
                <span class="text-gray-600">Purity:</span>
                <span class="font-medium">{{ product.purity }}</span>
              </div>
              <div v-if="product.occasion" class="flex justify-between">
                <span class="text-gray-600">Occasion:</span>
                <span class="font-medium">{{ product.occasion }}</span>
              </div>
            </div>
            
            <!-- Variants -->
            <div v-if="product.variants && product.variants.length" class="mb-6">
              <h3 class="font-medium text-gray-900 mb-3">Select Options</h3>
              <div class="space-y-3">
                <div 
                  v-for="variant in product.variants" 
                  :key="variant.id"
                  class="flex items-center space-x-3"
                >
                  <input 
                    type="radio"
                    :id="variant.id"
                    :value="variant.id"
                    v-model="selectedVariant"
                    class="text-rose-gold focus:ring-rose-gold"
                  >
                  <label :for="variant.id" class="flex-1">
                    <span class="font-medium">{{ variant.name }}: {{ variant.value }}</span>
                    <span v-if="variant.price_adjustment > 0" class="text-sm text-gray-500 ml-2">
                      (+₹{{ formatPrice(variant.price_adjustment) }})
                    </span>
                  </label>
                </div>
              </div>
            </div>
            
            <!-- Quantity -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-900 mb-2">Quantity</label>
              <div class="flex items-center space-x-3">
                <button 
                  @click="decreaseQuantity"
                  :disabled="quantity <= 1"
                  class="w-8 h-8 border border-gray-300 rounded-lg flex items-center justify-center disabled:opacity-50"
                >
                  <Icon name="heroicons:minus" class="w-4 h-4" />
                </button>
                <input 
                  v-model.number="quantity"
                  type="number"
                  min="1"
                  class="w-16 text-center border border-gray-300 rounded-lg py-2"
                >
                <button 
                  @click="increaseQuantity"
                  class="w-8 h-8 border border-gray-300 rounded-lg flex items-center justify-center"
                >
                  <Icon name="heroicons:plus" class="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <!-- Actions -->
            <div class="flex space-x-3 mb-6">
              <button 
                @click="addToCart"
                :disabled="!product.is_in_stock"
                class="flex-1 btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Icon name="heroicons:shopping-cart" class="w-5 h-5 mr-2" />
                Add to Cart
              </button>
              <button 
                @click="addToWishlist"
                class="w-12 h-12 border border-gray-300 rounded-lg flex items-center justify-center hover:border-rose-gold transition-colors"
                :class="{ 'text-rose-gold': isInWishlist }"
              >
                <Icon 
                  :name="isInWishlist ? 'heroicons:heart' : 'heroicons:heart'" 
                  class="w-5 h-5"
                  :class="{ 'fill-current': isInWishlist }"
                />
              </button>
            </div>
            
            <!-- Stock Status -->
            <div class="mb-6">
              <div v-if="product.is_in_stock" class="flex items-center text-green-600">
                <Icon name="heroicons:check-circle" class="w-5 h-5 mr-2" />
                <span>In Stock</span>
              </div>
              <div v-else class="flex items-center text-red-600">
                <Icon name="heroicons:x-circle" class="w-5 h-5 mr-2" />
                <span>Out of Stock</span>
              </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="flex space-x-4 text-sm">
              <NuxtLink 
                :to="`/products/${product.slug}`"
                class="text-rose-gold hover:text-deep-maroon transition-colors"
              >
                View Full Details
              </NuxtLink>
              <button class="text-gray-500 hover:text-gray-700 transition-colors">
                Share
              </button>
            </div>
          </div>
        </div>
      </div>
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
const emit = defineEmits(['close', 'add-to-cart'])

// Reactive state
const quantity = ref(1)
const selectedVariant = ref(null)
const currentImageIndex = ref(0)

// Computed
const currentImage = computed(() => {
  if (props.product.images && props.product.images.length > currentImageIndex.value) {
    return props.product.images[currentImageIndex.value].image_url
  }
  return props.product.main_image
})

// Methods
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN').format(price)
}

const increaseQuantity = () => {
  quantity.value++
}

const decreaseQuantity = () => {
  if (quantity.value > 1) {
    quantity.value--
  }
}

const nextImage = () => {
  if (props.product.images && props.product.images.length > 1) {
    currentImageIndex.value = (currentImageIndex.value + 1) % props.product.images.length
  }
}

const previousImage = () => {
  if (props.product.images && props.product.images.length > 1) {
    currentImageIndex.value = currentImageIndex.value === 0 
      ? props.product.images.length - 1 
      : currentImageIndex.value - 1
  }
}

const addToCart = () => {
  if (props.product.is_in_stock) {
    emit('add-to-cart', {
      ...props.product,
      quantity: quantity.value,
      selectedVariant: selectedVariant.value
    })
    emit('close')
  }
}

// Import wishlist composable
import { useWishlist } from '~/composables/useWishlist'

// Use wishlist composable
const { isInWishlist, toggleWishlist } = useWishlist()

const addToWishlist = async () => {
  await toggleWishlist(props.product)
}

// Initialize
onMounted(() => {
  if (props.product.variants && props.product.variants.length > 0) {
    selectedVariant.value = props.product.variants[0].id
  }
})
</script>