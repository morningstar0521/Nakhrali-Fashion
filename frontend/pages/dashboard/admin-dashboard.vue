<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">Admin Dashboard</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Welcome back, {{ userFullName }}!</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <!-- Admin Stats -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:users" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalUsers }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:shopping-bag" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Orders</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalOrders }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:tag" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Products</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">{{ stats.totalProducts }}</p>
            </div>
          </div>
        </div>

        <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 dark:bg-rose-gold/20 rounded-lg">
              <Icon name="ph:currency-inr" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600 dark:text-gray-400">Total Revenue</p>
              <p class="text-2xl font-bold text-gray-900 dark:text-white">₹{{ stats.totalRevenue }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Orders -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow mb-8">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-xl font-display text-deep-maroon dark:text-rose-gold">Recent Orders</h2>
        </div>
        <div class="p-6">
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
              <thead>
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Order #</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Customer</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Total</th>
                  <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                <tr v-for="order in recentOrders" :key="order.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ order.orderNumber }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ order.customerName }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ formatDate(order.date) }}</td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusClass(order.status)">
                      {{ order.status }}
                    </span>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">₹{{ order.total }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <NuxtLink :to="`/dashboard/admin/orders/${order.id}`" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">View</NuxtLink>
                  </td>
                </tr>
                <tr v-if="recentOrders.length === 0">
                  <td colspan="6" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">No orders found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 text-right">
          <NuxtLink to="/dashboard/admin/orders" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 text-sm font-medium">View All Orders</NuxtLink>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Content Management -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-display text-deep-maroon dark:text-rose-gold">Content Management</h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 gap-4">
              <NuxtLink to="/dashboard/admin/products" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:tag" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Products</span>
              </NuxtLink>
              
              <NuxtLink to="/dashboard/admin/categories" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:folders" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Categories</span>
              </NuxtLink>
              
              <NuxtLink to="/dashboard/admin/collections" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:stack" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Collections</span>
              </NuxtLink>
              
              <NuxtLink to="/dashboard/admin/pages" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:file-text" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Pages</span>
              </NuxtLink>
            </div>
          </div>
        </div>
        
        <!-- User Management -->
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h2 class="text-xl font-display text-deep-maroon dark:text-rose-gold">User Management</h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-1 gap-4">
              <NuxtLink to="/dashboard/admin/users" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:users" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Users</span>
              </NuxtLink>
              
              <NuxtLink to="/dashboard/admin/roles" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:user-gear" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Roles</span>
              </NuxtLink>
              
              <NuxtLink to="/dashboard/admin/reviews" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:star" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Manage Reviews</span>
              </NuxtLink>
              
              <NuxtLink to="/dashboard/admin/settings" class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:border-rose-gold dark:hover:border-rose-gold hover:bg-rose-gold/5 dark:hover:bg-rose-gold/10 transition-colors">
                <Icon name="ph:gear" class="w-5 h-5 text-rose-gold mr-3" />
                <span class="font-medium text-gray-900 dark:text-white">Site Settings</span>
              </NuxtLink>
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
  title: 'Admin Dashboard - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Admin dashboard for Nakhrali Fashion - manage products, orders, users, and more.'
    }
  ]
})

// Auth
const { user, userFullName, isAdmin } = useAuth()

// Apply admin middleware
definePageMeta({
  middleware: 'admin'
})

// Stats
const stats = ref({
  totalUsers: 0,
  totalOrders: 0,
  totalProducts: 0,
  totalRevenue: 0
})

// Recent orders
const recentOrders = ref([])

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

// Fetch admin dashboard data
const fetchDashboardData = async () => {
  try {
    // In a real application, this would be an API call
    // For now, we'll use mock data
    stats.value = {
      totalUsers: 124,
      totalOrders: 56,
      totalProducts: 89,
      totalRevenue: '4,56,789'
    }
    
    recentOrders.value = [
      {
        id: '1',
        orderNumber: 'NK20230501123456',
        customerName: 'Priya Sharma',
        date: '2023-05-01',
        status: 'delivered',
        total: '12,499'
      },
      {
        id: '2',
        orderNumber: 'NK20230502123457',
        customerName: 'Rahul Patel',
        date: '2023-05-02',
        status: 'shipped',
        total: '8,999'
      },
      {
        id: '3',
        orderNumber: 'NK20230503123458',
        customerName: 'Ananya Singh',
        date: '2023-05-03',
        status: 'processing',
        total: '15,999'
      },
      {
        id: '4',
        orderNumber: 'NK20230504123459',
        customerName: 'Vikram Malhotra',
        date: '2023-05-04',
        status: 'placed',
        total: '6,499'
      },
      {
        id: '5',
        orderNumber: 'NK20230505123460',
        customerName: 'Neha Gupta',
        date: '2023-05-05',
        status: 'confirmed',
        total: '9,999'
      }
    ]
  } catch (error) {
    console.error('Error fetching dashboard data:', error)
  }
}

// Fetch data on component mount
onMounted(fetchDashboardData)
</script>