<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">My Dashboard</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Welcome back, {{ user.firstName }}!</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Sidebar Navigation -->
        <div class="lg:col-span-1">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <div class="flex items-center">
                <div class="h-12 w-12 rounded-full bg-rose-gold/10 flex items-center justify-center text-deep-maroon dark:text-rose-gold">
                  <span class="text-xl font-medium">{{ userInitials }}</span>
                </div>
                <div class="ml-3">
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ user.firstName }} {{ user.lastName }}</p>
                  <p class="text-xs text-gray-500 dark:text-gray-400">{{ user.email }}</p>
                </div>
              </div>
            </div>
            <nav class="space-y-1 p-2">
              <NuxtLink 
                v-for="item in navigationItems" 
                :key="item.name"
                :to="item.href"
                class="flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors" 
                :class="[item.current ? 'bg-rose-gold/10 text-deep-maroon dark:text-rose-gold' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700']"
              >
                <Icon :name="item.icon" class="mr-3 h-5 w-5" />
                {{ item.name }}
              </NuxtLink>
            </nav>
          </div>
        </div>

        <!-- Main Content -->
        <div class="lg:col-span-3">
          <!-- Overview Cards -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center">
                  <Icon name="ph:shopping-bag" class="h-5 w-5 text-blue-600 dark:text-blue-300" />
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ stats.orders }}</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Orders Placed</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center">
                  <Icon name="ph:heart" class="h-5 w-5 text-purple-600 dark:text-purple-300" />
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ stats.wishlist }}</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Wishlist Items</p>
                </div>
              </div>
            </div>
            
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
              <div class="flex items-center">
                <div class="flex-shrink-0 h-10 w-10 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center">
                  <Icon name="ph:tag" class="h-5 w-5 text-green-600 dark:text-green-300" />
                </div>
                <div class="ml-4">
                  <h3 class="text-lg font-medium text-gray-900 dark:text-white">{{ stats.reviews }}</h3>
                  <p class="text-sm text-gray-500 dark:text-gray-400">Reviews Written</p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Recent Orders -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden mb-8">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Recent Orders</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Track your recent purchases</p>
            </div>
            
            <div class="overflow-x-auto">
              <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead>
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Order #</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Total</th>
                    <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                  </tr>
                </thead>
                <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  <tr v-for="order in recentOrders" :key="order.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ order.orderNumber }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ formatDate(order.date) }}</td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusClass(order.status)">
                        {{ order.status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">₹{{ order.total }}</td>
                    <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <NuxtLink :to="`/dashboard/orders/${order.id}`" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">
                        View
                      </NuxtLink>
                    </td>
                  </tr>
                  <tr v-if="recentOrders.length === 0">
                    <td colspan="5" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                      No orders found
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            
            <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
              <NuxtLink to="/dashboard/orders" class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 flex items-center">
                View all orders
                <Icon name="ph:arrow-right" class="ml-1 h-4 w-4" />
              </NuxtLink>
            </div>
          </div>
          
          <!-- Wishlist Preview -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden mb-8">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Wishlist</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Items you've saved for later</p>
            </div>
            
            <div class="p-4">
              <div v-if="wishlistItems.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                <div v-for="item in wishlistItems.slice(0, 3)" :key="item.id" class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                  <div class="h-48 bg-gray-200 dark:bg-gray-700 relative">
                    <img :src="item.image" :alt="item.name" class="w-full h-full object-cover" />
                    <button @click="removeFromWishlist(item.id)" class="absolute top-2 right-2 h-8 w-8 rounded-full bg-white dark:bg-gray-800 flex items-center justify-center text-red-500 hover:text-red-600 shadow-sm">
                      <Icon name="ph:heart-fill" class="h-5 w-5" />
                    </button>
                  </div>
                  <div class="p-4">
                    <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ item.name }}</h4>
                    <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">₹{{ item.price }}</p>
                    <button @click="addToCart(item)" class="mt-3 w-full px-3 py-1.5 bg-rose-gold hover:bg-deep-maroon text-white text-sm rounded-md">
                      Add to Cart
                    </button>
                  </div>
                </div>
              </div>
              
              <div v-else class="text-center py-8">
                <Icon name="ph:heart" class="h-12 w-12 mx-auto text-gray-400" />
                <h3 class="mt-2 text-sm font-medium text-gray-900 dark:text-white">No items in wishlist</h3>
                <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Start adding items to your wishlist</p>
                <div class="mt-6">
                  <NuxtLink to="/products" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
                    Browse Products
                  </NuxtLink>
                </div>
              </div>
            </div>
            
            <div v-if="wishlistItems.length > 0" class="px-6 py-4 border-t border-gray-200 dark:border-gray-700">
              <NuxtLink to="/dashboard/wishlist" class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 flex items-center">
                View all wishlist items
                <Icon name="ph:arrow-right" class="ml-1 h-4 w-4" />
              </NuxtLink>
            </div>
          </div>
          
          <!-- Account Information -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <div class="px-4 py-5 sm:px-6 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Account Information</h3>
              <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">Personal details and preferences</p>
            </div>
            
            <div class="p-6">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-3">Personal Information</h4>
                  <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400">First Name</p>
                        <p class="text-sm font-medium text-gray-900 dark:text-white">{{ user.firstName }}</p>
                      </div>
                      <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Last Name</p>
                        <p class="text-sm font-medium text-gray-900 dark:text-white">{{ user.lastName }}</p>
                      </div>
                      <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Email</p>
                        <p class="text-sm font-medium text-gray-900 dark:text-white">{{ user.email }}</p>
                      </div>
                      <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400">Phone</p>
                        <p class="text-sm font-medium text-gray-900 dark:text-white">{{ user.phone }}</p>
                      </div>
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-600">
                      <NuxtLink to="/dashboard/profile" class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">
                        Edit Profile
                      </NuxtLink>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-3">Default Address</h4>
                  <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <div v-if="user.defaultAddress">
                      <p class="text-sm text-gray-900 dark:text-white">{{ user.defaultAddress.line1 }}</p>
                      <p v-if="user.defaultAddress.line2" class="text-sm text-gray-900 dark:text-white">{{ user.defaultAddress.line2 }}</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ user.defaultAddress.city }}, {{ user.defaultAddress.state }} {{ user.defaultAddress.postalCode }}</p>
                      <p class="text-sm text-gray-900 dark:text-white">{{ user.defaultAddress.country }}</p>
                    </div>
                    <div v-else class="text-sm text-gray-500 dark:text-gray-400">
                      No default address set
                    </div>
                    <div class="mt-4 pt-3 border-t border-gray-200 dark:border-gray-600">
                      <NuxtLink to="/dashboard/addresses" class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">
                        Manage Addresses
                      </NuxtLink>
                    </div>
                  </div>
                </div>
              </div>
              
              <div class="mt-6">
                <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-3">Account Security</h4>
                <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                  <div class="flex items-center justify-between">
                    <div>
                      <p class="text-sm font-medium text-gray-900 dark:text-white">Password</p>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">Last updated: {{ formatDate(user.passwordUpdatedAt) }}</p>
                    </div>
                    <NuxtLink to="/dashboard/change-password" class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">
                      Change Password
                    </NuxtLink>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'My Dashboard - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'View your orders, wishlist, and account information.'
    }
  ]
})

// Auth
const { isAuthenticated } = useAuth()

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
})

// Mock user data
const user = ref({
  firstName: 'Priya',
  lastName: 'Sharma',
  email: 'priya@example.com',
  phone: '+91 98765 43210',
  passwordUpdatedAt: '2023-03-15',
  defaultAddress: {
    line1: '123 Main Street',
    line2: 'Apartment 4B',
    city: 'Mumbai',
    state: 'Maharashtra',
    postalCode: '400001',
    country: 'India'
  }
})

// Computed properties
const userInitials = computed(() => {
  return `${user.value.firstName.charAt(0)}${user.value.lastName.charAt(0)}`
})

// Navigation items
const navigationItems = [
  { name: 'Dashboard', href: '/dashboard/user-dashboard', icon: 'ph:house', current: true },
  { name: 'Orders', href: '/dashboard/orders', icon: 'ph:shopping-bag', current: false },
  { name: 'Wishlist', href: '/dashboard/wishlist', icon: 'ph:heart', current: false },
  { name: 'Reviews', href: '/dashboard/reviews', icon: 'ph:star', current: false },
  { name: 'Addresses', href: '/dashboard/addresses', icon: 'ph:map-pin', current: false },
  { name: 'Profile', href: '/dashboard/profile', icon: 'ph:user', current: false },
  { name: 'Change Password', href: '/dashboard/change-password', icon: 'ph:lock', current: false },
]

// Stats
const stats = ref({
  orders: 5,
  wishlist: 8,
  reviews: 3
})

// Recent orders
const recentOrders = ref([
  {
    id: '1',
    orderNumber: 'NK20230501123456',
    date: '2023-05-01',
    status: 'delivered',
    total: '12,499'
  },
  {
    id: '2',
    orderNumber: 'NK20230415123457',
    date: '2023-04-15',
    status: 'shipped',
    total: '8,999'
  },
  {
    id: '3',
    orderNumber: 'NK20230320123458',
    date: '2023-03-20',
    status: 'delivered',
    total: '15,999'
  }
])

// Wishlist items
const wishlistItems = ref([
  {
    id: '1',
    name: 'Elegant Pearl Necklace',
    price: '4,999',
    image: 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: '2',
    name: 'Diamond Stud Earrings',
    price: '3,500',
    image: 'https://images.unsplash.com/photo-1629224316810-9d8805b95e76?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  },
  {
    id: '3',
    name: 'Gold Chain Bracelet',
    price: '6,499',
    image: 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
  }
])

// Methods
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

const getStatusClass = (status) => {
  const statusClasses = {
    'placed': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-300',
    'confirmed': 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-300',
    'processing': 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300',
    'shipped': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-300',
    'delivered': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300',
    'cancelled': 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300'
  }
  return statusClasses[status] || 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300'
}

const removeFromWishlist = (id) => {
  wishlistItems.value = wishlistItems.value.filter(item => item.id !== id)
  stats.value.wishlist = wishlistItems.value.length
}

const addToCart = (item) => {
  // In a real application, this would add the item to the cart
  alert(`Added ${item.name} to cart`)
}
</script>