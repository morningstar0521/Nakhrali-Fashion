<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <!-- Page Header -->
      <div class="mb-8 text-center md:text-left">
        <h1 class="text-3xl font-display font-bold text-deep-maroon mb-2">
          My Orders
        </h1>
        <p class="text-gray-600">
          Track and manage your orders
        </p>
      </div>
      
      <!-- Orders List -->
      <div class="bg-white rounded-lg shadow-md border border-gray-100 overflow-hidden">
        <!-- Filters -->
        <div class="p-4 border-b border-gray-100 bg-gray-50 flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center space-x-2">
            <select 
              v-model="filters.status" 
              class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
            >
              <option value="">All Orders</option>
              <option value="pending">Pending</option>
              <option value="processing">Processing</option>
              <option value="shipped">Shipped</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
            
            <select 
              v-model="filters.timeframe" 
              class="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
            >
              <option value="">All Time</option>
              <option value="30">Last 30 Days</option>
              <option value="90">Last 3 Months</option>
              <option value="365">Last Year</option>
            </select>
          </div>
          
          <div class="relative">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Icon name="ph:magnifying-glass" class="h-5 w-5 text-gray-400" />
            </div>
            <input
              v-model="filters.search"
              type="text"
              placeholder="Search orders..."
              class="pl-10 px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-transparent"
            />
          </div>
        </div>
        
        <!-- Orders Table -->
        <div class="overflow-x-auto">
          <table v-if="filteredOrders.length > 0" class="min-w-full divide-y divide-gray-200">
            <thead class="bg-gray-50">
              <tr>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Order #
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Date
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Status
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Total
                </th>
                <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Items
                </th>
                <th scope="col" class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Actions
                </th>
              </tr>
            </thead>
            <tbody class="bg-white divide-y divide-gray-200">
              <tr v-for="order in filteredOrders" :key="order.id" class="hover:bg-gray-50">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                  {{ order.orderNumber }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ formatDate(order.date) }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusClass(order.status)">
                    {{ order.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  ₹{{ order.total }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {{ order.itemCount }} {{ order.itemCount === 1 ? 'item' : 'items' }}
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <NuxtLink :to="`/dashboard/orders/${order.id}`" class="text-rose-gold hover:text-deep-maroon">
                    View
                  </NuxtLink>
                </td>
              </tr>
            </tbody>
          </table>
          
          <!-- Empty State -->
          <div v-else class="p-8 text-center">
            <div class="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
              <Icon name="ph:shopping-bag" class="h-8 w-8 text-gray-400" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-1">No orders found</h3>
            <p class="text-gray-500 mb-4">{{ getEmptyStateMessage() }}</p>
            <NuxtLink to="/products" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
              Browse Products
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Back to Dashboard Link -->
      <div class="mt-6 text-center">
        <NuxtLink to="/dashboard" class="text-rose-gold hover:text-deep-maroon transition-colors inline-flex items-center">
          <Icon name="ph:arrow-left" class="mr-1 h-4 w-4" />
          Back to Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { format, parseISO, subDays } from 'date-fns';

// SEO
useHead({
  title: 'My Orders - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'View and track your Nakhrali Fashion orders.'
    }
  ]
});

// Auth
const { user } = useAuth();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;

// Orders data
const orders = ref([]);
const isLoading = ref(false);

// Filters
const filters = reactive({
  status: '',
  timeframe: '',
  search: ''
});

// Mock data for demo
const mockOrders = [
  {
    id: 1,
    orderNumber: 'NF-2023-001',
    status: 'Delivered',
    date: '2023-05-15T10:30:00Z',
    itemCount: 2,
    total: '12,999'
  },
  {
    id: 2,
    orderNumber: 'NF-2023-002',
    status: 'Processing',
    date: '2023-06-02T14:45:00Z',
    itemCount: 1,
    total: '8,499'
  },
  {
    id: 3,
    orderNumber: 'NF-2023-003',
    status: 'Shipped',
    date: '2023-06-10T09:15:00Z',
    itemCount: 3,
    total: '24,999'
  },
  {
    id: 4,
    orderNumber: 'NF-2023-004',
    status: 'Pending',
    date: '2023-06-15T16:20:00Z',
    itemCount: 1,
    total: '6,499'
  },
  {
    id: 5,
    orderNumber: 'NF-2023-005',
    status: 'Cancelled',
    date: '2023-06-08T11:30:00Z',
    itemCount: 2,
    total: '15,999'
  }
];

// Load orders
onMounted(async () => {
  isLoading.value = true;
  
  try {
    // In a real app, fetch from API
    // const response = await $fetch(`${apiBase}/orders`, {
    //   method: 'GET',
    //   headers: {
    //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    //   }
    // });
    // orders.value = response.orders;
    
    // Using mock data for demo
    setTimeout(() => {
      orders.value = mockOrders;
      isLoading.value = false;
    }, 500);
  } catch (error) {
    console.error('Failed to load orders:', error);
    isLoading.value = false;
  }
});

// Filtered orders
const filteredOrders = computed(() => {
  let result = [...orders.value];
  
  // Filter by status
  if (filters.status) {
    result = result.filter(order => 
      order.status.toLowerCase() === filters.status.toLowerCase()
    );
  }
  
  // Filter by timeframe
  if (filters.timeframe) {
    const days = parseInt(filters.timeframe);
    const cutoffDate = subDays(new Date(), days);
    
    result = result.filter(order => {
      const orderDate = parseISO(order.date);
      return orderDate >= cutoffDate;
    });
  }
  
  // Filter by search
  if (filters.search) {
    const searchTerm = filters.search.toLowerCase();
    result = result.filter(order => 
      order.orderNumber.toLowerCase().includes(searchTerm)
    );
  }
  
  return result;
});

// Format date
const formatDate = (dateString) => {
  try {
    return format(parseISO(dateString), 'MMM d, yyyy');
  } catch (error) {
    return dateString;
  }
};

// Get status class
const getStatusClass = (status) => {
  switch (status.toLowerCase()) {
    case 'delivered':
      return 'bg-green-100 text-green-800';
    case 'processing':
      return 'bg-blue-100 text-blue-800';
    case 'shipped':
      return 'bg-indigo-100 text-indigo-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'cancelled':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Get empty state message
const getEmptyStateMessage = () => {
  if (filters.status || filters.timeframe || filters.search) {
    return 'Try adjusting your filters to find what you\'re looking for';
  }
  return 'You haven\'t placed any orders yet';
};

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
});
</script>