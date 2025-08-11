<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Track Your Order</h1>

    <!-- Order lookup form -->
    <div v-if="!orderDetails && !isLoading" class="max-w-md mx-auto bg-white rounded-lg shadow-sm p-6 mb-8">
      <p class="text-gray-600 mb-6">Enter your order number and email to track your order status</p>
      
      <form @submit.prevent="trackOrder" class="space-y-4">
        <div>
          <label for="order_number" class="block text-gray-700 mb-1">Order Number</label>
          <input 
            id="order_number"
            v-model="orderNumber"
            type="text"
            class="w-full px-3 py-2 border rounded-md"
            placeholder="e.g. NF12345"
            required
          >
        </div>
        
        <div>
          <label for="email" class="block text-gray-700 mb-1">Email Address</label>
          <input 
            id="email"
            v-model="email"
            type="email"
            class="w-full px-3 py-2 border rounded-md"
            placeholder="Enter the email used for your order"
            required
          >
        </div>
        
        <button 
          type="submit"
          class="w-full bg-primary text-white py-2 rounded-md hover:bg-primary-dark transition"
          :disabled="isLoading"
        >
          <span v-if="isLoading">Searching...</span>
          <span v-else>Track Order</span>
        </button>
      </form>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error state -->
    <div v-if="error" class="max-w-3xl mx-auto bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
      <button @click="resetTracking" class="ml-2 underline">Try again</button>
    </div>

    <!-- Order details -->
    <div v-if="orderDetails && !isLoading" class="max-w-3xl mx-auto">
      <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl font-semibold">Order #{{ orderDetails.order_number }}</h2>
          <span class="px-2 py-1 rounded text-xs font-medium" :class="{
            'bg-blue-100 text-blue-800': orderDetails.status === 'processing',
            'bg-yellow-100 text-yellow-800': orderDetails.status === 'packed',
            'bg-purple-100 text-purple-800': orderDetails.status === 'shipped',
            'bg-green-100 text-green-800': orderDetails.status === 'delivered',
            'bg-red-100 text-red-800': orderDetails.status === 'cancelled'
          }">
            {{ formatOrderStatus(orderDetails.status) }}
          </span>
        </div>

        <div class="border-b pb-4 mb-4">
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Order Date</span>
            <span>{{ formatDate(orderDetails.created_at) }}</span>
          </div>
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Total Amount</span>
            <span class="font-medium">{{ formatPrice(orderDetails.total) }}</span>
          </div>
          <div class="flex justify-between mb-2">
            <span class="text-gray-600">Payment Method</span>
            <span>{{ formatPaymentMethod(orderDetails.payment_method) }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-600">Payment Status</span>
            <span :class="{
              'text-green-600': orderDetails.payment_status === 'paid',
              'text-yellow-600': orderDetails.payment_status === 'pending',
              'text-red-600': orderDetails.payment_status === 'failed'
            }">
              {{ formatPaymentStatus(orderDetails.payment_status) }}
            </span>
          </div>
        </div>

        <!-- Shipping tracking info -->
        <div v-if="trackingInfo" class="mb-6">
          <h3 class="font-medium mb-3">Shipping Details</h3>
          
          <div class="space-y-2 mb-4">
            <div class="flex justify-between">
              <span class="text-gray-600">Courier</span>
              <span>{{ trackingInfo.courier_name }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Tracking Number</span>
              <a 
                :href="trackingInfo.tracking_url" 
                target="_blank" 
                class="text-primary hover:underline"
              >
                {{ trackingInfo.tracking_number }}
              </a>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Estimated Delivery</span>
              <span>{{ trackingInfo.estimated_delivery_date ? formatDate(trackingInfo.estimated_delivery_date) : 'Not available' }}</span>
            </div>
          </div>
          
          <!-- Tracking timeline -->
          <div class="relative pl-8 space-y-6 mt-6">
            <!-- Vertical line -->
            <div class="absolute top-0 left-3 bottom-0 w-0.5 bg-gray-200"></div>
            
            <div v-for="(event, index) in trackingInfo.shipment_track" :key="index" class="relative">
              <!-- Status dot -->
              <div class="absolute -left-8 mt-1.5 w-6 h-6 rounded-full flex items-center justify-center" :class="{
                'bg-green-100': event.status_type === 'delivered',
                'bg-blue-100': event.status_type === 'in_transit',
                'bg-yellow-100': event.status_type === 'pending',
                'bg-gray-100': event.status_type === 'exception'
              }">
                <div class="w-2 h-2 rounded-full" :class="{
                  'bg-green-600': event.status_type === 'delivered',
                  'bg-blue-600': event.status_type === 'in_transit',
                  'bg-yellow-600': event.status_type === 'pending',
                  'bg-gray-600': event.status_type === 'exception'
                }"></div>
              </div>
              
              <div>
                <div class="font-medium">{{ event.status }}</div>
                <div class="text-sm text-gray-600">{{ formatDate(event.date) }}</div>
                <div v-if="event.location" class="text-sm text-gray-600">{{ event.location }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Delivery progress bar (if no detailed tracking) -->
        <div v-else class="mb-6">
          <h3 class="font-medium mb-3">Delivery Status</h3>
          
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

        <!-- Order items -->
        <div>
          <h3 class="font-medium mb-3">Items in Your Order</h3>
          <div v-for="item in orderDetails.items" :key="item.id" class="flex py-3 border-b last:border-b-0">
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
      </div>

      <div class="text-center">
        <button @click="resetTracking" class="bg-white border border-gray-300 px-6 py-2 rounded-md hover:bg-gray-50 transition">
          Track Another Order
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { useShipping } from '~/composables/useShipping'

const toast = useToast()
const config = useRuntimeConfig()
const { getTrackingInfo, isLoading: isShippingLoading, error: shippingError } = useShipping()

// State
const orderNumber = ref('')
const email = ref('')
const isLoading = ref(false)
const error = ref(null)
const orderDetails = ref(null)
const trackingInfo = ref(null)

// Track order
const trackOrder = async () => {
  if (!orderNumber.value || !email.value) {
    toast.error('Please enter both order number and email')
    return
  }
  
  isLoading.value = true
  error.value = null
  
  try {
    // In a real application, this would be an API call
    // For now, we'll use mock data
    await new Promise(resolve => setTimeout(resolve, 1500)) // Simulate API delay
    
    // This would be the actual API call
    // const response = await $fetch(`${config.public.apiBase}/orders/track`, {
    //   method: 'POST',
    //   body: {
    //     order_number: orderNumber.value,
    //     email: email.value
    //   }
    // })
    // orderDetails.value = response
    
    // Mock data for demonstration
    if (orderNumber.value.toLowerCase() === 'nf12345') {
      orderDetails.value = {
        id: '12345',
        order_number: 'NF12345',
        created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
        status: 'shipped',
        payment_method: 'credit_card',
        payment_status: 'paid',
        shipping_method: 'express',
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
        shipping: 199,
        tax: 6300,
        total: 41497
      }
      
      // Get tracking info
      await fetchTrackingInfo(orderDetails.value.id)
    } else {
      error.value = 'Order not found. Please check your order number and email.'
    }
  } catch (err) {
    console.error('Error tracking order:', err)
    error.value = 'Failed to track order. Please try again.'
  } finally {
    isLoading.value = false
  }
}

// Fetch tracking info
const fetchTrackingInfo = async (orderId) => {
  try {
    // In a real application, this would call the useShipping composable
    // const response = await getTrackingInfo(orderId)
    // trackingInfo.value = response
    
    // Mock data for demonstration
    trackingInfo.value = {
      courier_name: 'Delhivery',
      tracking_number: 'DEL1234567890',
      tracking_url: 'https://www.delhivery.com/track',
      estimated_delivery_date: new Date(Date.now() + 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days from now
      shipment_track: [
        {
          status: 'Order Placed',
          status_type: 'pending',
          date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(), // 5 days ago
          location: 'Mumbai'
        },
        {
          status: 'Order Processed',
          status_type: 'pending',
          date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000).toISOString(), // 4 days ago
          location: 'Mumbai'
        },
        {
          status: 'Shipped',
          status_type: 'in_transit',
          date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
          location: 'Mumbai'
        },
        {
          status: 'In Transit',
          status_type: 'in_transit',
          date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(), // 2 days ago
          location: 'Delhi'
        },
        {
          status: 'Out for Delivery',
          status_type: 'in_transit',
          date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
          location: 'Bangalore'
        }
      ]
    }
  } catch (err) {
    console.error('Error fetching tracking info:', err)
    // Don't set error here to avoid disrupting the user experience
  }
}

// Reset tracking form
const resetTracking = () => {
  orderNumber.value = ''
  email.value = ''
  orderDetails.value = null
  trackingInfo.value = null
  error.value = null
}

// Delivery steps
const deliverySteps = [
  {
    status: 'processing',
    label: 'Order Placed',
    icon: 'svg-icon-shopping-bag',
    date: orderDetails.value?.created_at
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
  const currentStatusIndex = statusOrder.indexOf(orderDetails.value?.status)
  const stepStatusIndex = statusOrder.indexOf(status)
  
  return currentStatusIndex >= stepStatusIndex
}

// Get progress bar width
const getProgressWidth = () => {
  const statusOrder = ['processing', 'packed', 'shipped', 'delivered']
  const currentStatusIndex = statusOrder.indexOf(orderDetails.value?.status)
  
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