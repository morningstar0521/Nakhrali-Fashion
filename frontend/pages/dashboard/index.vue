<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">Dashboard</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Welcome back, {{ userFullName }}!</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Quick Stats -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:shopping-bag" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Orders</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ orderStats.total }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:heart" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Wishlist Items</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ wishlistCount }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:map-pin" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Saved Addresses</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ addressCount }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Order History -->
      <div class="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
          <h2 class="text-xl font-display text-deep-maroon dark:text-rose-gold">My Orders</h2>
          <NuxtLink to="/dashboard/orders" class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 font-medium">View All</NuxtLink>
        </div>
        
        <div class="p-6">
          <!-- Order Grid -->
          <div v-if="orders.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="order in orders" :key="order.id" class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow">
              <!-- Order Header -->
              <div class="px-4 py-3 bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600 flex justify-between items-center">
                <span class="font-medium text-gray-900 dark:text-white">{{ order.orderNumber }}</span>
                <span class="px-2 py-1 text-xs rounded-full" :class="getStatusClass(order.status)">
                  {{ order.status }}
                </span>
              </div>
              
              <!-- Order Images -->
              <div class="p-4 border-b border-gray-200 dark:border-gray-700">
                <div class="flex space-x-2 overflow-x-auto pb-2">
                  <div v-for="(item, index) in order.items" :key="index" class="flex-shrink-0 relative">
                    <img :src="item.image" :alt="item.name" class="h-16 w-16 object-cover rounded-md border border-gray-200 dark:border-gray-600" />
                    <span v-if="item.quantity > 1" class="absolute -top-2 -right-2 bg-rose-gold text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">{{ item.quantity }}</span>
                  </div>
                </div>
              </div>
              
              <!-- Order Details -->
              <div class="p-4">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm text-gray-500 dark:text-gray-400">{{ formatDate(order.date) }}</span>
                  <span class="font-medium text-gray-900 dark:text-white">₹{{ order.total }}</span>
                </div>
                <div class="text-sm text-gray-500 dark:text-gray-400 mb-4">
                  {{ order.itemCount }} {{ order.itemCount === 1 ? 'item' : 'items' }}
                </div>
                <NuxtLink :to="`/dashboard/orders/${order.id}`" class="block w-full text-center py-2 px-4 bg-rose-gold/10 hover:bg-rose-gold/20 text-rose-gold rounded-md transition-colors text-sm font-medium">
                  View Details
                </NuxtLink>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-else class="text-center py-8">
            <Icon name="ph:shopping-bag" class="w-12 h-12 text-gray-400 dark:text-gray-500 mx-auto mb-4" />
            <p class="text-gray-500 dark:text-gray-400">You haven't placed any orders yet</p>
            <NuxtLink to="/products" class="mt-4 inline-block px-4 py-2 bg-rose-gold text-white rounded-md hover:bg-deep-maroon transition-colors">
              Start Shopping
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-8 bg-white dark:bg-gray-800 rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-display text-deep-maroon dark:text-rose-gold">Quick Actions</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <NuxtLink
              to="/products"
              class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors"
            >
              <Icon name="ph:shopping-bag" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium text-gray-900 dark:text-white">Shop Now</span>
            </NuxtLink>

            <NuxtLink
              to="/dashboard/profile"
              class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors"
            >
              <Icon name="ph:user" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium text-gray-900 dark:text-white">My Profile</span>
            </NuxtLink>

            <NuxtLink
              to="/dashboard/orders"
              class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors"
            >
              <Icon name="ph:package" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium text-gray-900 dark:text-white">My Orders</span>
            </NuxtLink>

            <NuxtLink
              to="/wishlist"
              class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors"
            >
              <Icon name="ph:heart" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium text-gray-900 dark:text-white">Wishlist</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Dashboard - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Your Nakhrali Fashion dashboard - manage your account, view orders, and explore our jewelry collections.'
    }
  ]
})

const { user, userFullName, isAdmin } = useAuth()
const router = useRouter()

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
})

// Redirect admin users to admin dashboard
onMounted(() => {
  if (isAdmin.value) {
    router.push('/dashboard/admin-dashboard')
  }
})

// Stats
const orderStats = ref({ total: 0, completed: 0, processing: 0 })
const wishlistCount = ref(0)
const addressCount = ref(0)

// Orders
const orders = ref([])

// Format date
const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })
}

// Get status class
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

// Fetch user dashboard data
const fetchDashboardData = async () => {
  try {
    // In a real application, this would be an API call
    // For now, we'll use mock data
    orderStats.value = { total: 3, completed: 1, processing: 2 }
    wishlistCount.value = 5
    addressCount.value = 1
    
    orders.value = [
      {
        id: '1',
        orderNumber: 'NK20230501123456',
        date: '2023-05-01',
        status: 'delivered',
        total: '12,499',
        itemCount: 2,
        items: [
          {
            id: '1',
            name: 'Gold Plated Kundan Necklace',
            image: '/images/products/necklace1.jpg',
            quantity: 1
          },
          {
            id: '2',
            name: 'Pearl Drop Earrings',
            image: '/images/products/earrings1.jpg',
            quantity: 1
          }
        ]
      },
      {
        id: '2',
        orderNumber: 'NK20230502123457',
        date: '2023-05-15',
        status: 'shipped',
        total: '8,999',
        itemCount: 1,
        items: [
          {
            id: '3',
            name: 'Rose Gold Bangle Set',
            image: '/images/products/bangles1.jpg',
            quantity: 1
          }
        ]
      },
      {
        id: '3',
        orderNumber: 'NK20230503123458',
        date: '2023-05-28',
        status: 'processing',
        total: '15,999',
        itemCount: 3,
        items: [
          {
            id: '4',
            name: 'Diamond Studded Ring',
            image: '/images/products/ring1.jpg',
            quantity: 1
          },
          {
            id: '5',
            name: 'Silver Anklet',
            image: '/images/products/anklet1.jpg',
            quantity: 1
          },
          {
            id: '6',
            name: 'Traditional Maang Tikka',
            image: '/images/products/maangtikka1.jpg',
            quantity: 1
          }
        ]
      }
    ]
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

// Fetch data on component mount
onMounted(fetchDashboardData)
</script>