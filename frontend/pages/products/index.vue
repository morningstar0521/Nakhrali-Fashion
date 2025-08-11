<template>
  <div class="min-h-screen bg-ivory">
    <!-- Page Header -->
    <section class="bg-white py-8 border-b border-gray-200">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-display text-gray-900 mb-2">All Products</h1>
            <p class="text-gray-600">
              {{ totalProducts }} products found
            </p>
          </div>
          
          <!-- Sort Options -->
          <div class="flex items-center space-x-4">
            <select 
              v-model="sortBy"
              @change="updateProducts"
              class="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent"
            >
              <option value="created_at">Latest</option>
              <option value="name">Name A-Z</option>
              <option value="price">Price Low to High</option>
              <option value="price_desc">Price High to Low</option>
              <option value="rating">Highest Rated</option>
            </select>
            
            <!-- View Toggle -->
            <div class="flex border border-gray-300 rounded-lg">
              <button 
                @click="viewMode = 'grid'"
                class="p-2 transition-colors"
                :class="viewMode === 'grid' ? 'bg-rose-gold text-white' : 'text-gray-600 hover:text-rose-gold'"
              >
                <Icon name="heroicons:squares-2x2" class="w-5 h-5" />
              </button>
              <button 
                @click="viewMode = 'list'"
                class="p-2 transition-colors"
                :class="viewMode === 'list' ? 'bg-rose-gold text-white' : 'text-gray-600 hover:text-rose-gold'"
              >
                <Icon name="heroicons:bars-3" class="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="container mx-auto px-4 py-8">
      <div class="flex flex-col lg:flex-row gap-8">
        <!-- Filters Sidebar -->
        <div class="lg:w-1/4">
          <div class="bg-white rounded-xl shadow-soft p-6 sticky top-24">
            <h3 class="text-lg font-display text-gray-900 mb-6">Filters</h3>
            
            <!-- Categories -->
            <div class="mb-6">
              <h4 class="font-medium text-gray-900 mb-3">Categories</h4>
              <div class="space-y-2">
                <label 
                  v-for="category in categories" 
                  :key="category.id"
                  class="flex items-center space-x-2 cursor-pointer"
                >
                  <input 
                    type="checkbox"
                    :value="category.id"
                    v-model="selectedCategories"
                    @change="updateProducts"
                    class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                  >
                  <span class="text-gray-700">{{ category.name }}</span>
                </label>
              </div>
            </div>

            <!-- Price Range -->
            <div class="mb-6">
              <h4 class="font-medium text-gray-900 mb-3">Price Range</h4>
              <div class="space-y-3">
                <div>
                  <label class="block text-sm text-gray-600 mb-1">Min Price</label>
                  <input 
                    v-model.number="priceRange.min"
                    type="number"
                    placeholder="0"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent"
                  >
                </div>
                <div>
                  <label class="block text-sm text-gray-600 mb-1">Max Price</label>
                  <input 
                    v-model.number="priceRange.max"
                    type="number"
                    placeholder="50000"
                    class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent"
                  >
                </div>
                <button 
                  @click="updateProducts"
                  class="w-full btn-primary text-sm"
                >
                  Apply Price Filter
                </button>
              </div>
            </div>

            <!-- Material -->
            <div class="mb-6">
              <h4 class="font-medium text-gray-900 mb-3">Material</h4>
              <div class="space-y-2">
                <label 
                  v-for="material in materials" 
                  :key="material"
                  class="flex items-center space-x-2 cursor-pointer"
                >
                  <input 
                    type="checkbox"
                    :value="material"
                    v-model="selectedMaterials"
                    @change="updateProducts"
                    class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                  >
                  <span class="text-gray-700">{{ material }}</span>
                </label>
              </div>
            </div>

            <!-- Occasion -->
            <div class="mb-6">
              <h4 class="font-medium text-gray-900 mb-3">Occasion</h4>
              <div class="space-y-2">
                <label 
                  v-for="occasion in occasions" 
                  :key="occasion"
                  class="flex items-center space-x-2 cursor-pointer"
                >
                  <input 
                    type="checkbox"
                    :value="occasion"
                    v-model="selectedOccasions"
                    @change="updateProducts"
                    class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                  >
                  <span class="text-gray-700">{{ occasion }}</span>
                </label>
              </div>
            </div>

            <!-- Availability -->
            <div class="mb-6">
              <h4 class="font-medium text-gray-900 mb-3">Availability</h4>
              <div class="space-y-2">
                <label class="flex items-center space-x-2 cursor-pointer">
                  <input 
                    type="checkbox"
                    v-model="inStockOnly"
                    @change="updateProducts"
                    class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                  >
                  <span class="text-gray-700">In Stock Only</span>
                </label>
              </div>
            </div>

            <!-- Clear Filters -->
            <button 
              @click="clearFilters"
              class="w-full btn-outline text-sm"
            >
              Clear All Filters
            </button>
          </div>
        </div>

        <!-- Products Grid -->
        <div class="lg:w-3/4">
          <!-- Loading State -->
          <div v-if="loading" class="text-center py-12">
            <div class="spinner w-8 h-8 mx-auto mb-4"></div>
            <p class="text-gray-600">Loading products...</p>
          </div>

          <!-- Products Grid -->
          <div v-else-if="products.length" class="space-y-6">
            <div 
              :class="viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6' : 'space-y-4'"
            >
              <ProductCard 
                v-for="product in products" 
                :key="product.id"
                :product="product"
                @add-to-cart="addToCart"
                @add-to-wishlist="addToWishlist"
                @quick-view="quickView"
              />
            </div>

            <!-- Pagination -->
            <div v-if="totalPages > 1" class="flex justify-center mt-8">
              <nav class="flex items-center space-x-2">
                <button 
                  @click="changePage(currentPage - 1)"
                  :disabled="currentPage === 1"
                  class="px-3 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  <Icon name="heroicons:chevron-left" class="w-4 h-4" />
                </button>
                
                <button 
                  v-for="page in visiblePages" 
                  :key="page"
                  @click="changePage(page)"
                  class="px-3 py-2 border rounded-lg transition-colors"
                  :class="page === currentPage ? 'bg-rose-gold text-white border-rose-gold' : 'border-gray-300 hover:bg-gray-50'"
                >
                  {{ page }}
                </button>
                
                <button 
                  @click="changePage(currentPage + 1)"
                  :disabled="currentPage === totalPages"
                  class="px-3 py-2 border border-gray-300 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
                >
                  <Icon name="heroicons:chevron-right" class="w-4 h-4" />
                </button>
              </nav>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="text-center py-12">
            <Icon name="heroicons:inbox" class="w-16 h-16 text-gray-400 mx-auto mb-4" />
            <h3 class="text-lg font-display text-gray-900 mb-2">No products found</h3>
            <p class="text-gray-600 mb-6">
              Try adjusting your filters or search terms
            </p>
            <button 
              @click="clearFilters"
              class="btn-primary"
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick View Modal -->
    <QuickViewModal 
      v-if="showQuickView"
      :product="selectedProduct"
      @close="showQuickView = false"
      @add-to-cart="addToCart"
    />
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'All Products - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Browse our complete collection of ethnic jewelry. Rings, earrings, necklaces, bangles, and more. Premium quality jewelry for every occasion.'
    }
  ]
})

// Route and query params
const route = useRoute()
const router = useRouter()

// Reactive state
const products = ref([])
const categories = ref([])
const loading = ref(false)
const totalProducts = ref(0)
const totalPages = ref(1)
const currentPage = ref(1)
const viewMode = ref('grid')
const showQuickView = ref(false)
const selectedProduct = ref(null)

// Filters
const selectedCategories = ref([])
const selectedMaterials = ref([])
const selectedOccasions = ref([])
const priceRange = ref({ min: null, max: null })
const inStockOnly = ref(false)
const sortBy = ref('created_at')

// Sample data
const materials = ['Gold', 'Silver', 'Platinum', 'Diamond', 'Pearl', 'Gemstone']
const occasions = ['Bridal', 'Casual', 'Party', 'Office', 'Festival', 'Traditional']

// Computed
const visiblePages = computed(() => {
  const pages = []
  const start = Math.max(1, currentPage.value - 2)
  const end = Math.min(totalPages.value, currentPage.value + 2)
  
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  
  return pages
})

// Methods
const loadProducts = async () => {
  loading.value = true
  
  try {
    const params = {
      page: currentPage.value,
      per_page: 12,
      sort_by: sortBy.value,
      ...(selectedCategories.value.length && { category_id: selectedCategories.value.join(',') }),
      ...(selectedMaterials.value.length && { material: selectedMaterials.value.join(',') }),
      ...(selectedOccasions.value.length && { occasion: selectedOccasions.value.join(',') }),
      ...(priceRange.value.min && { min_price: priceRange.value.min }),
      ...(priceRange.value.max && { max_price: priceRange.value.max }),
      ...(inStockOnly.value && { in_stock: true })
    }
    
    // API call
    // const response = await $fetch('/api/products', { params })
    // products.value = response.products
    // totalProducts.value = response.pagination.total
    // totalPages.value = response.pagination.total_pages
    
    // For now, use sample data
    products.value = []
    totalProducts.value = 0
    totalPages.value = 1
  } catch (error) {
    console.error('Failed to load products:', error)
  } finally {
    loading.value = false
  }
}

const updateProducts = () => {
  currentPage.value = 1
  loadProducts()
}

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadProducts()
  }
}

const clearFilters = () => {
  selectedCategories.value = []
  selectedMaterials.value = []
  selectedOccasions.value = []
  priceRange.value = { min: null, max: null }
  inStockOnly.value = false
  sortBy.value = 'created_at'
  updateProducts()
}

const addToCart = (product) => {
  // Will be implemented with cart store
  console.log('Add to cart:', product)
}

const addToWishlist = (product) => {
  // Will be implemented with wishlist store
  console.log('Add to wishlist:', product)
}

const quickView = (product) => {
  selectedProduct.value = product
  showQuickView.value = true
}

// Load data on mount
onMounted(() => {
  loadProducts()
})

// Watch for route changes
watch(() => route.query, () => {
  // Update filters based on route query params
  if (route.query.category) {
    selectedCategories.value = [route.query.category]
  }
  if (route.query.search) {
    // Handle search
  }
  loadProducts()
}, { immediate: true })
</script> 