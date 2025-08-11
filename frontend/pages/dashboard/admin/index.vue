<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-7xl mx-auto">
      <!-- Dashboard Header -->
      <div class="mb-10 text-center md:text-left">
        <h1 class="text-3xl md:text-4xl font-display font-bold text-deep-maroon mb-2">
          Admin Dashboard
        </h1>
        <p class="text-gray-600">
          Manage your store, products, orders, and customers.
        </p>
      </div>
      
      <!-- Dashboard Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Store Summary Card -->
        <div class="bg-white rounded-lg shadow-md p-6 border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="bg-rose-gold/10 p-3 rounded-full mr-4">
              <Icon name="ph:storefront" class="h-6 w-6 text-rose-gold" />
            </div>
            <h2 class="text-xl font-display font-semibold">Store Overview</h2>
          </div>
          <div class="space-y-4">
            <div class="flex justify-between items-center">
              <span class="text-gray-600">Total Products</span>
              <span class="font-semibold">124</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-600">Total Orders</span>
              <span class="font-semibold">56</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-600">Total Customers</span>
              <span class="font-semibold">89</span>
            </div>
            <div class="flex justify-between items-center">
              <span class="text-gray-600">Total Revenue</span>
              <span class="font-semibold">₹4,56,789</span>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-gray-100">
            <NuxtLink to="/dashboard/admin/analytics" class="text-rose-gold hover:text-deep-maroon text-sm font-medium transition-colors flex items-center justify-center">
              View Detailed Analytics
              <Icon name="ph:arrow-right" class="ml-1 h-4 w-4" />
            </NuxtLink>
          </div>
        </div>
        
        <!-- Recent Orders Card -->
        <div class="bg-white rounded-lg shadow-md p-6 border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="bg-rose-gold/10 p-3 rounded-full mr-4">
              <Icon name="ph:shopping-bag" class="h-6 w-6 text-rose-gold" />
            </div>
            <h2 class="text-xl font-display font-semibold">Recent Orders</h2>
          </div>
          <div class="space-y-3">
            <div v-for="order in recentOrders" :key="order.id" class="p-3 border border-gray-100 rounded-lg">
              <div class="flex justify-between items-center">
                <span class="font-medium">{{ order.orderNumber }}</span>
                <span class="text-xs px-2 py-1 rounded-full" :class="getStatusClass(order.status)">
                  {{ order.status }}
                </span>
              </div>
              <div class="text-sm text-gray-500 mt-1">
                {{ formatDate(order.date) }} · ₹{{ order.total }}
              </div>
              <div class="text-sm mt-1">
                {{ order.customerName }}
              </div>
            </div>
          </div>
          <div class="mt-4 pt-3 border-t border-gray-100">
            <NuxtLink to="/dashboard/admin/orders" class="text-rose-gold hover:text-deep-maroon text-sm font-medium transition-colors flex items-center justify-center">
              Manage All Orders
              <Icon name="ph:arrow-right" class="ml-1 h-4 w-4" />
            </NuxtLink>
          </div>
        </div>
        
        <!-- Quick Actions Card -->
        <div class="bg-white rounded-lg shadow-md p-6 border border-gray-100">
          <div class="flex items-center mb-4">
            <div class="bg-rose-gold/10 p-3 rounded-full mr-4">
              <Icon name="ph:lightning" class="h-6 w-6 text-rose-gold" />
            </div>
            <h2 class="text-xl font-display font-semibold">Quick Actions</h2>
          </div>
          <div class="grid grid-cols-1 gap-3">
            <NuxtLink to="/dashboard/admin/products/create" class="flex items-center p-3 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors">
              <Icon name="ph:plus-circle" class="h-5 w-5 text-rose-gold mr-2" />
              <span>Add New Product</span>
            </NuxtLink>
            <NuxtLink to="/dashboard/admin/products" class="flex items-center p-3 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors">
              <Icon name="ph:list" class="h-5 w-5 text-rose-gold mr-2" />
              <span>Manage Products</span>
            </NuxtLink>
            <NuxtLink to="/dashboard/admin/users" class="flex items-center p-3 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors">
              <Icon name="ph:users" class="h-5 w-5 text-rose-gold mr-2" />
              <span>Manage Users</span>
            </NuxtLink>
            <NuxtLink to="/dashboard/admin/settings" class="flex items-center p-3 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors">
              <Icon name="ph:gear" class="h-5 w-5 text-rose-gold mr-2" />
              <span>Store Settings</span>
            </NuxtLink>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="mt-8 bg-white rounded-lg shadow-md p-6 border border-gray-100">
        <div class="flex items-center mb-4">
          <div class="bg-rose-gold/10 p-3 rounded-full mr-4">
            <Icon name="ph:activity" class="h-6 w-6 text-rose-gold" />
          </div>
          <h2 class="text-xl font-display font-semibold">Recent Activity</h2>
        </div>
        <div class="space-y-4">
          <div v-for="activity in recentActivity" :key="activity.id" class="flex items-start">
            <div class="bg-gray-100 rounded-full p-2 mr-3">
              <Icon :name="getActivityIcon(activity.type)" class="h-5 w-5 text-gray-600" />
            </div>
            <div>
              <p class="text-sm">{{ activity.message }}</p>
              <p class="text-xs text-gray-500">{{ formatDate(activity.date) }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { format, parseISO } from 'date-fns';

// SEO
useHead({
  title: 'Admin Dashboard - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Admin dashboard for Nakhrali Fashion - manage products, orders, and users.'
    }
  ]
});

// Auth
const { user, userFullName, isAdmin } = useAuth();

// Mock data for demo
const recentOrders = ref([
  {
    id: 1,
    orderNumber: 'NF-2023-001',
    status: 'Delivered',
    date: '2023-05-15T10:30:00Z',
    total: '12,999',
    customerName: 'Priya Sharma'
  },
  {
    id: 2,
    orderNumber: 'NF-2023-002',
    status: 'Processing',
    date: '2023-06-02T14:45:00Z',
    total: '8,499',
    customerName: 'Rahul Patel'
  },
  {
    id: 3,
    orderNumber: 'NF-2023-003',
    status: 'Pending',
    date: '2023-06-05T09:15:00Z',
    total: '24,999',
    customerName: 'Ananya Desai'
  }
]);

const recentActivity = ref([
  {
    id: 1,
    type: 'product',
    message: 'New product "Diamond Studded Gold Earrings" was added',
    date: '2023-06-05T14:30:00Z'
  },
  {
    id: 2,
    type: 'order',
    message: 'Order #NF-2023-003 status changed to "Processing"',
    date: '2023-06-05T12:45:00Z'
  },
  {
    id: 3,
    type: 'user',
    message: 'New user "Ananya Desai" registered',
    date: '2023-06-05T10:15:00Z'
  },
  {
    id: 4,
    type: 'payment',
    message: 'Payment received for order #NF-2023-002',
    date: '2023-06-04T16:20:00Z'
  }
]);

// Format date
const formatDate = (dateString) => {
  try {
    return format(parseISO(dateString), 'MMM d, yyyy h:mm a');
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
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'cancelled':
      return 'bg-red-100 text-red-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

// Get activity icon
const getActivityIcon = (type) => {
  switch (type) {
    case 'order':
      return 'ph:shopping-bag';
    case 'product':
      return 'ph:package';
    case 'user':
      return 'ph:user-circle';
    case 'payment':
      return 'ph:credit-card';
    default:
      return 'ph:bell';
  }
};

// Apply admin middleware
definePageMeta({
  middleware: 'admin'
});
</script>