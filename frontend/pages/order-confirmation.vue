<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Success state -->
    <div v-else class="max-w-3xl mx-auto">
      <div class="text-center mb-8">
        <div class="inline-flex items-center justify-center w-24 h-24 bg-green-100 rounded-full mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <h1 class="text-3xl font-bold mb-2">Order Confirmed!</h1>
        <p class="text-gray-600 text-lg">Thank you for shopping with Nakhrali Fashion</p>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Order Details</h2>
          <span class="text-sm text-gray-500">Order #{{ order.order_number }}</span>
        </div>

        <div class="border-b pb-4 mb-4">
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Order Date</span>
            <span>{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Payment Method</span>
            <span>{{ formatPaymentMethod(order.payment_method) }}</span>
          </div>
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Payment Status</span>
            <span :class="{
              'text-green-600': order.payment_status === 'paid',
              'text-yellow-600': order.payment_status === 'pending',
              'text-red-600': order.payment_status === 'failed'
            }">
              {{ formatPaymentStatus(order.payment_status) }}
            </span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Order Status</span>
            <span class="px-2 py-1 rounded text-xs font-medium" :class="{
              'bg-blue-100 text-blue-800': order.status === 'processing',
              'bg-yellow-100 text-yellow-800': order.status === 'packed',
              'bg-purple-100 text-purple-800': order.status === 'shipped',
              'bg-green-100 text-green-800': order.status === 'delivered',
              'bg-red-100 text-red-800': order.status === 'cancelled'
            }">
              {{ formatOrderStatus(order.status) }}
            </span>
          </div>
        </div>

        <div class="mb-6">
          <h3 class="font-medium mb-3">Items</h3>
          <div v-for="item in order.items" :key="item.id" class="flex py-3 border-b last:border-b-0">
            <img 
              :src="item.product.main_image" 
              :alt="item.product.name"
              class="w-16 h-16 object-cover rounded-md"
            >
            <div class="ml-3 flex-1">
              <div class="font-medium">{{ item.product.name }}</div>
              <div v-if="item.variant" class="text-sm text-gray-600">
                {{ formatVariantOptions(item.variant) }}
              </div>
              <div class="flex justify-between mt-1">
                <div class="text-sm">Qty: {{ item.quantity }}</div>
                <div class="font-medium">{{ formatPrice(item.price * item.quantity) }}</div>
              </div>
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 class="font-medium mb-3">Shipping Address</h3>
            <div class="text-gray-600">
              <div class="font-medium text-gray-800">{{ order.shipping_address.full_name }}</div>
              <div>{{ order.shipping_address.street_address }}</div>
              <div>{{ order.shipping_address.city }}, {{ order.shipping_address.state }} {{ order.shipping_address.postal_code }}</div>
              <div>{{ order.shipping_address.country }}</div>
              <div class="mt-1">{{ order.shipping_address.phone_number }}</div>
            </div>
          </div>

          <div>
            <h3 class="font-medium mb-3">Order Summary</h3>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600">Subtotal</span>
                <span>{{ formatPrice(order.subtotal) }}</span>
              </div>
              <div v-if="order.discount > 0" class="flex justify-between text-green-600">
                <span>Discount</span>
                <span>-{{ formatPrice(order.discount) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Shipping</span>
                <span>{{ formatPrice(order.shipping) }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600">Tax</span>
                <span>{{ formatPrice(order.tax) }}</span>
              </div>
              <div class="flex justify-between font-bold text-lg pt-2 border-t">
                <span>Total</span>
                <span>{{ formatPrice(order.total) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <h2 class="text-xl font-semibold mb-4">Delivery Information</h2>
        
        <div class="relative">
          <!-- Progress bar -->
          <div class="hidden md:block h-1 bg-gray-200 absolute top-5 left-0 right-0 mx-12">
            <div class="h-full bg-primary" :style="{ width: getProgressWidth() }"></div>
          </div>
          
          <!-- Status steps -->
          <div class="flex flex-col md:flex-row justify-between">
            <div 
              v-for="(step, index) in deliverySteps" 
              :key="step.status"
              class="flex flex-row md:flex-col items-center md:items-center mb-4 md:mb-0"
              :class="{'opacity-50': !isStepCompleted(step.status)}"
            >
              <div class="relative flex items-center justify-center w-10 h-10 rounded-full bg-white border-2 z-10"
                :class="isStepCompleted(step.status) ? 'border-primary text-primary' : 'border-gray-300 text-gray-400'">
                <component :is="step.icon" class="w-5 h-5" />
              </div>
              <div class="ml-3 md:ml-0 md:mt-2 text-center">
                <div class="font-medium" :class="isStepCompleted(step.status) ? 'text-primary' : 'text-gray-500'">
                  {{ step.label }}
                </div>
                <div v-if="isStepCompleted(step.status) && step.date" class="text-xs text-gray-500">
                  {{ formatDate(step.date) }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="text-center">
        <NuxtLink to="/products" class="inline-block bg-primary text-white px-6 py-2 rounded-md hover:bg-primary-dark transition mr-4">
          Continue Shopping
        </NuxtLink>
        <NuxtLink to="/dashboard" class="inline-block bg-white border border-gray-300 px-6 py-2 rounded-md hover:bg-gray-50 transition">
          View All Orders
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuth } from '~/composables/useAuth'

const route = useRoute()
const router = useRouter()
const toast = useToast()
const config = useRuntimeConfig()
const { isAuthenticated, accessToken } = useAuth()

// State
const isLoading = ref(true)
const error = ref(null)
const order = ref(null)

// Fetch order details
onMounted(async () => {
  if (!isAuthenticated.value) {
    toast.error('Please log in to view your order')
    router.push('/login?redirect=/order-confirmation')
    return
  }

  const orderId = route.query.id
  if (!orderId) {
    error.value = 'Order ID is missing'
    isLoading.value = false
    return
  }

  try {
    // In a real application, this would be an API call
    // For now, we'll use mock data
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulate API delay
    
    // This would be the actual API call
    // const response = await $fetch(`${config.public.apiBase}/orders/${orderId}`, {
    //   method: 'GET',
    //   headers: {
    //     'Authorization': `Bearer ${accessToken.value}`
    //   }
    // })
    // order.value = response

    // Mock data for demonstration
    order.value = {
      id: orderId,
      order_number: 'NF' + String(Math.floor(Math.random() * 10000)).padStart(5, '0'),
      created_at: new Date().toISOString(),
      status: 'processing',
      payment_method: 'credit_card',
      payment_status: 'paid',
      shipping_method: 'standard',
      shipping_address: {
        full_name: 'John Doe',
        phone_number: '+91 9876543210',
        street_address: '123 Main Street',
        city: 'Mumbai',
        state: 'Maharashtra',
        postal_code: '400001',
        country: 'India'
      },
      items: [
        {
          id: '1',
          product: {
            id: '101',
            name: 'Diamond Studded Gold Ring',
            main_image: 'https://via.placeholder.com/150?text=Ring',
            slug: 'diamond-studded-gold-ring'
          },
          variant: {
            id: '1001',
            options: {
              size: '16mm',
              metal: '18K Gold'
            },
            price: 24999
          },
          quantity: 1,
          price: 24999
        },
        {
          id: '2',
          product: {
            id: '102',
            name: 'Pearl Necklace',
            main_image: 'https://via.placeholder.com/150?text=Necklace',
            slug: 'pearl-necklace'
          },
          variant: null,
          quantity: 1,
          price: 12999
        }
      ],
      subtotal: 37998,
      discount: 3000,
      shipping: 99,
      tax: 6300,
      total: 41397
    }
  } catch (err) {
    console.error('Error fetching order:', err)
    error.value = 'Failed to load order details'
  } finally {
    isLoading.value = false
  }
})

// Delivery steps
const deliverySteps = [
  {
    status: 'processing',
    label: 'Order Placed',
    icon: 'svg-icon-shopping-bag',
    date: order.value?.created_at
  },
  {
    status: 'packed',
    label: 'Order Packed',
    icon: 'svg-icon-package',
    date: null
  },
  {
    status: 'shipped',
    label: 'Order Shipped',
    icon: 'svg-icon-truck',
    date: null
  },
  {
    status: 'delivered',
    label: 'Order Delivered',
    icon: 'svg-icon-check-circle',
    date: null
  }
]

// Check if a step is completed
const isStepCompleted = (status) => {
  const statusOrder = ['processing', 'packed', 'shipped', 'delivered']
  const currentStatusIndex = statusOrder.indexOf(order.value?.status)
  const stepStatusIndex = statusOrder.indexOf(status)
  
  return currentStatusIndex >= stepStatusIndex
}

// Get progress bar width
const getProgressWidth = () => {
  const statusOrder = ['processing', 'packed', 'shipped', 'delivered']
  const currentStatusIndex = statusOrder.indexOf(order.value?.status)
  
  if (currentStatusIndex < 0) return '0%'
  
  const progress = (currentStatusIndex / (statusOrder.length - 1)) * 100
  return `${progress}%`
}

// Format date
const formatDate = (dateString) => {
  if (!dateString) return ''
  
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('en-IN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date)
}

// Format payment method
const formatPaymentMethod = (method) => {
  const methods = {
    'credit_card': 'Credit/Debit Card',
    'upi': 'UPI',
    'cod': 'Cash on Delivery'
  }
  
  return methods[method] || method
}

// Format payment status
const formatPaymentStatus = (status) => {
  const statuses = {
    'paid': 'Paid',
    'pending': 'Pending',
    'failed': 'Failed'
  }
  
  return statuses[status] || status
}

// Format order status
const formatOrderStatus = (status) => {
  const statuses = {
    'processing': 'Processing',
    'packed': 'Packed',
    'shipped': 'Shipped',
    'delivered': 'Delivered',
    'cancelled': 'Cancelled'
  }
  
  return statuses[status] || status
}

// Format price
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR'
  }).format(price)
}

// Format variant options
const formatVariantOptions = (variant) => {
  if (!variant || !variant.options) return ''
  
  return Object.entries(variant.options)
    .map(([key, value]) => `${key}: ${value}`)
    .join(', ')
}
</script>

<script>
// Define SVG icons as components
export default {
  components: {
    'svg-icon-shopping-bag': {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
        </svg>
      `
    },
    'svg-icon-package': {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10" />
        </svg>
      `
    },
    'svg-icon-truck': {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
        </svg>
      `
    },
    'svg-icon-check-circle': {
      template: `
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      `
    }
  }
}
</script>