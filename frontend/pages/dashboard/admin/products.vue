<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">Product Management</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Manage your product catalog</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Actions Bar -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
        <div class="flex items-center space-x-2">
          <div class="relative">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Search products..."
              class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              @input="handleSearch"
            />
            <div class="absolute left-3 top-2.5">
              <Icon name="ph:magnifying-glass" class="h-5 w-5 text-gray-400 dark:text-gray-500" />
            </div>
          </div>

          <select
            v-model="filters.category"
            class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Categories</option>
            <option value="necklaces">Necklaces</option>
            <option value="earrings">Earrings</option>
            <option value="rings">Rings</option>
            <option value="bracelets">Bracelets</option>
            <option value="anklets">Anklets</option>
          </select>

          <select
            v-model="filters.status"
            class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="draft">Draft</option>
            <option value="out_of_stock">Out of Stock</option>
          </select>
        </div>

        <button
          @click="showAddProductModal = true"
          class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg flex items-center justify-center transition-colors"
        >
          <Icon name="ph:plus" class="mr-2 h-5 w-5" />
          Add New Product
        </button>
      </div>

      <!-- Products Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <div v-for="product in paginatedProducts" :key="product.id" class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden border border-gray-200 dark:border-gray-700 hover:border-rose-gold dark:hover:border-rose-gold transition-colors">
          <div class="relative pb-[100%] bg-gray-100 dark:bg-gray-700">
            <img 
              :src="product.image" 
              :alt="product.name" 
              class="absolute inset-0 w-full h-full object-cover"
            />
            <div class="absolute top-2 right-2 flex space-x-1">
              <button @click="editProduct(product)" class="p-1.5 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-rose-gold hover:text-white transition-colors">
                <Icon name="ph:pencil" class="h-4 w-4" />
              </button>
              <button @click="confirmDeleteProduct(product)" class="p-1.5 bg-white dark:bg-gray-800 rounded-full shadow hover:bg-red-500 hover:text-white transition-colors">
                <Icon name="ph:trash" class="h-4 w-4" />
              </button>
            </div>
            <div v-if="product.status !== 'active'" class="absolute top-2 left-2 px-2 py-1 text-xs font-semibold rounded-full" :class="getStatusBadgeClass(product.status)">
              {{ formatStatus(product.status) }}
            </div>
          </div>
          <div class="p-4">
            <h3 class="text-lg font-medium text-gray-900 dark:text-white truncate">{{ product.name }}</h3>
            <div class="flex items-center justify-between mt-1">
              <div class="text-rose-gold font-semibold">₹{{ formatPrice(product.price) }}</div>
              <div class="text-sm text-gray-500 dark:text-gray-400">{{ product.sku }}</div>
            </div>
            <div class="mt-2 flex items-center text-sm text-gray-500 dark:text-gray-400">
              <Icon name="ph:tag" class="h-4 w-4 mr-1" />
              <span>{{ product.category }}</span>
            </div>
            <div class="mt-1 flex items-center text-sm text-gray-500 dark:text-gray-400">
              <Icon name="ph:cube" class="h-4 w-4 mr-1" />
              <span>Stock: {{ product.stock }}</span>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="paginatedProducts.length === 0" class="col-span-full py-12 flex flex-col items-center justify-center text-gray-500 dark:text-gray-400">
          <Icon name="ph:shopping-bag" class="h-16 w-16 mb-4 opacity-30" />
          <h3 class="text-lg font-medium">No products found</h3>
          <p class="mt-1">Try adjusting your search or filters</p>
        </div>
      </div>

      <!-- Pagination -->
      <div class="mt-8 flex items-center justify-between">
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Showing <span class="font-medium">{{ paginationStart }}</span> to <span class="font-medium">{{ paginationEnd }}</span> of <span class="font-medium">{{ totalProducts }}</span> products
        </div>
        <div class="flex space-x-2">
          <button 
            @click="currentPage--" 
            :disabled="currentPage === 1" 
            class="px-3 py-1 rounded-md border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Previous
          </button>
          <button 
            @click="currentPage++" 
            :disabled="paginationEnd >= totalProducts" 
            class="px-3 py-1 rounded-md border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Next
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Product Modal -->
    <div v-if="showAddProductModal || showEditProductModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h3 class="text-xl font-display text-deep-maroon dark:text-rose-gold">
            {{ showEditProductModal ? 'Edit Product' : 'Add New Product' }}
          </h3>
          <button @click="closeProductModal" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <Icon name="ph:x" class="h-5 w-5" />
          </button>
        </div>
        <div class="p-6">
          <form @submit.prevent="showEditProductModal ? updateProduct() : addProduct()">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Product Name</label>
                <input 
                  type="text" 
                  v-model="productForm.name" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">SKU</label>
                <input 
                  type="text" 
                  v-model="productForm.sku" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Price (₹)</label>
                <input 
                  type="number" 
                  v-model="productForm.price" 
                  required
                  min="0"
                  step="0.01"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Category</label>
                <select 
                  v-model="productForm.category" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                >
                  <option value="necklaces">Necklaces</option>
                  <option value="earrings">Earrings</option>
                  <option value="rings">Rings</option>
                  <option value="bracelets">Bracelets</option>
                  <option value="anklets">Anklets</option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Stock Quantity</label>
                <input 
                  type="number" 
                  v-model="productForm.stock" 
                  required
                  min="0"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
                <select 
                  v-model="productForm.status" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                >
                  <option value="active">Active</option>
                  <option value="draft">Draft</option>
                  <option value="out_of_stock">Out of Stock</option>
                </select>
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                <textarea 
                  v-model="productForm.description" 
                  rows="4"
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                ></textarea>
              </div>
              
              <div class="md:col-span-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Image URL</label>
                <input 
                  type="text" 
                  v-model="productForm.image" 
                  required
                  class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                />
              </div>
            </div>
            
            <div class="mt-6 flex justify-end space-x-3">
              <button 
                type="button" 
                @click="closeProductModal" 
                class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                Cancel
              </button>
              <button 
                type="submit" 
                class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg"
              >
                {{ showEditProductModal ? 'Update Product' : 'Add Product' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-xl font-display text-deep-maroon dark:text-rose-gold">Confirm Delete</h3>
        </div>
        <div class="p-6">
          <p class="text-gray-700 dark:text-gray-300">Are you sure you want to delete the product <span class="font-medium">{{ productToDelete?.name }}</span>? This action cannot be undone.</p>
          
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              @click="showDeleteModal = false" 
              class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Cancel
            </button>
            <button 
              @click="deleteProduct()" 
              class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg"
            >
              Delete Product
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Product Management - Nakhrali Fashion Admin',
  meta: [
    {
      name: 'description',
      content: 'Manage your product catalog for Nakhrali Fashion.'
    }
  ]
})

// Auth
const { isAdmin } = useAuth()

// Apply admin middleware
definePageMeta({
  middleware: 'admin'
})

// State
const searchQuery = ref('')
const filters = ref({
  category: '',
  status: ''
})
const currentPage = ref(1)
const itemsPerPage = 12
const showAddProductModal = ref(false)
const showEditProductModal = ref(false)
const showDeleteModal = ref(false)
const productToDelete = ref(null)
const productForm = ref({
  id: null,
  name: '',
  sku: '',
  price: 0,
  category: 'necklaces',
  stock: 0,
  status: 'active',
  description: '',
  image: ''
})

// Mock data for products
const products = ref([
  {
    id: 1,
    name: 'Elegant Pearl Necklace',
    sku: 'NK-PEARL-001',
    price: 12999,
    category: 'necklaces',
    stock: 15,
    status: 'active',
    description: 'Beautiful pearl necklace with gold accents.',
    image: 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 2,
    name: 'Diamond Stud Earrings',
    sku: 'ER-DIAM-002',
    price: 8999,
    category: 'earrings',
    stock: 20,
    status: 'active',
    description: 'Classic diamond stud earrings in 18k gold setting.',
    image: 'https://images.unsplash.com/photo-1629224316810-9d8805b95e76?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 3,
    name: 'Sapphire Engagement Ring',
    sku: 'RG-SAPH-003',
    price: 24999,
    category: 'rings',
    stock: 8,
    status: 'active',
    description: 'Stunning sapphire ring surrounded by diamonds.',
    image: 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 4,
    name: 'Gold Chain Bracelet',
    sku: 'BR-GOLD-004',
    price: 6499,
    category: 'bracelets',
    stock: 0,
    status: 'out_of_stock',
    description: 'Delicate gold chain bracelet with charm.',
    image: 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 5,
    name: 'Silver Anklet with Bells',
    sku: 'AN-SILV-005',
    price: 3999,
    category: 'anklets',
    stock: 12,
    status: 'active',
    description: 'Traditional silver anklet with small bells.',
    image: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 6,
    name: 'Ruby Pendant Necklace',
    sku: 'NK-RUBY-006',
    price: 15999,
    category: 'necklaces',
    stock: 5,
    status: 'active',
    description: 'Elegant ruby pendant on a gold chain.',
    image: 'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 7,
    name: 'Emerald Drop Earrings',
    sku: 'ER-EMER-007',
    price: 18999,
    category: 'earrings',
    stock: 0,
    status: 'draft',
    description: 'Luxurious emerald drop earrings with diamond accents.',
    image: 'https://images.unsplash.com/photo-1635767798638-3e25273a8236?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: 8,
    name: 'Platinum Wedding Band',
    sku: 'RG-PLAT-008',
    price: 9999,
    category: 'rings',
    stock: 10,
    status: 'active',
    description: 'Classic platinum wedding band with matte finish.',
    image: 'https://images.unsplash.com/photo-1586104195538-050b9f9b589c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  }
])

// Computed properties
const filteredProducts = computed(() => {
  let result = [...products.value]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(product => 
      product.name.toLowerCase().includes(query) || 
      product.sku.toLowerCase().includes(query) ||
      product.description.toLowerCase().includes(query)
    )
  }
  
  // Apply category filter
  if (filters.value.category) {
    result = result.filter(product => product.category === filters.value.category)
  }
  
  // Apply status filter
  if (filters.value.status) {
    result = result.filter(product => product.status === filters.value.status)
  }
  
  return result
})

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProducts.value.slice(start, end)
})

const totalProducts = computed(() => filteredProducts.value.length)

const paginationStart = computed(() => {
  if (totalProducts.value === 0) return 0
  return (currentPage.value - 1) * itemsPerPage + 1
})

const paginationEnd = computed(() => {
  return Math.min(currentPage.value * itemsPerPage, totalProducts.value)
})

// Methods
const handleSearch = () => {
  currentPage.value = 1 // Reset to first page on search
}

const formatPrice = (price) => {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")
}

const formatStatus = (status) => {
  return status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())
}

const getStatusBadgeClass = (status) => {
  const statusClasses = {
    'active': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    'draft': 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
    'out_of_stock': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
  }
  return statusClasses[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const editProduct = (product) => {
  productForm.value = { ...product }
  showEditProductModal.value = true
}

const confirmDeleteProduct = (product) => {
  productToDelete.value = product
  showDeleteModal.value = true
}

const closeProductModal = () => {
  showAddProductModal.value = false
  showEditProductModal.value = false
  productForm.value = {
    id: null,
    name: '',
    sku: '',
    price: 0,
    category: 'necklaces',
    stock: 0,
    status: 'active',
    description: '',
    image: ''
  }
}

const addProduct = () => {
  // In a real application, this would be an API call
  const newProduct = {
    ...productForm.value,
    id: products.value.length + 1
  }
  
  products.value.push(newProduct)
  closeProductModal()
}

const updateProduct = () => {
  // In a real application, this would be an API call
  const index = products.value.findIndex(p => p.id === productForm.value.id)
  if (index !== -1) {
    products.value[index] = { ...productForm.value }
  }
  closeProductModal()
}

const deleteProduct = () => {
  // In a real application, this would be an API call
  if (productToDelete.value) {
    products.value = products.value.filter(p => p.id !== productToDelete.value.id)
    showDeleteModal.value = false
    productToDelete.value = null
  }
}
</script>