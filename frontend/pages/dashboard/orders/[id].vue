<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto">
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-gold"></div>
      </div>
      
      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="bg-red-50 border border-red-200 rounded-lg p-6 inline-block mx-auto">
          <div class="flex items-center justify-center mb-4">
            <Icon name="ph:warning-circle" class="h-10 w-10 text-red-500" />
          </div>
          <h2 class="text-lg font-medium text-red-800 mb-2">Order Not Found</h2>
          <p class="text-red-600 mb-4">{{ error }}</p>
          <NuxtLink to="/dashboard/orders" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
            Back to Orders
          </NuxtLink>
        </div>
      </div>
      
      <!-- Order Details -->
      <div v-else class="bg-white rounded-lg shadow-md overflow-hidden">
        <!-- Order Header -->
        <div class="border-b border-gray-200 bg-gray-50 p-6">
          <div class="flex flex-col md:flex-row md:justify-between md:items-center">
            <div>
              <h1 class="text-2xl font-display font-bold text-deep-maroon mb-1">
                Order #{{ order.orderNumber }}
              </h1>
              <p class="text-gray-500 text-sm">
                Placed on {{ formatDate(order.date) }}
              </p>
            </div>
            <div class="mt-4 md:mt-0">
              <span class="px-3 py-1 inline-flex text-sm leading-5 font-semibold rounded-full" :class="getStatusClass(order.status)">
                {{ order.status }}
              </span>
            </div>
          </div>
        </div>
        
        <!-- Order Content -->
        <div class="p-6">
          <!-- Order Summary -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            <!-- Shipping Info -->
            <div class="border border-gray-200 rounded-lg p-4">
              <h2 class="font-medium text-gray-900 mb-3 flex items-center">
                <Icon name="ph:truck" class="h-5 w-5 mr-2 text-gray-500" />
                Shipping Information
              </h2>
              <div class="text-sm text-gray-600">
                <p class="font-medium text-gray-900 mb-1">{{ order.shipping.name }}</p>
                <p>{{ order.shipping.address.line1 }}</p>
                <p v-if="order.shipping.address.line2">{{ order.shipping.address.line2 }}</p>
                <p>{{ order.shipping.address.city }}, {{ order.shipping.address.state }} {{ order.shipping.address.postalCode }}</p>
                <p>{{ order.shipping.address.country }}</p>
                <p class="mt-2">{{ order.shipping.phone }}</p>
              </div>
            </div>
            
            <!-- Payment Info -->
            <div class="border border-gray-200 rounded-lg p-4">
              <h2 class="font-medium text-gray-900 mb-3 flex items-center">
                <Icon name="ph:credit-card" class="h-5 w-5 mr-2 text-gray-500" />
                Payment Information
              </h2>
              <div class="text-sm text-gray-600">
                <p class="mb-1">Payment Method: <span class="font-medium text-gray-900">{{ order.payment.method }}</span></p>
                <p v-if="order.payment.cardLast4" class="mb-1">Card: <span class="font-medium text-gray-900">•••• {{ order.payment.cardLast4 }}</span></p>
                <p class="mb-1">Payment Status: <span class="font-medium text-gray-900">{{ order.payment.status }}</span></p>
                <p v-if="order.payment.transactionId" class="mb-1">Transaction ID: <span class="font-medium text-gray-900">{{ order.payment.transactionId }}</span></p>
              </div>
            </div>
          </div>
          
          <!-- Order Items -->
          <div class="mb-8">
            <h2 class="font-medium text-gray-900 mb-4 flex items-center">
              <Icon name="ph:shopping-bag" class="h-5 w-5 mr-2 text-gray-500" />
              Order Items
            </h2>
            <div class="border border-gray-200 rounded-lg overflow-hidden">
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Product
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Price
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Quantity
                      </th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Total
                      </th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="item in order.items" :key="item.id" class="hover:bg-gray-50">
                      <td class="px-6 py-4 whitespace-nowrap">
                        <div class="flex items-center">
                          <div class="h-16 w-16 flex-shrink-0 overflow-hidden rounded-md border border-gray-200">
                            <img :src="item.image" :alt="item.name" class="h-full w-full object-cover object-center" />
                          </div>
                          <div class="ml-4">
                            <div class="text-sm font-medium text-gray-900">{{ item.name }}</div>
                            <div v-if="item.variant" class="text-sm text-gray-500">{{ item.variant }}</div>
                          </div>
                        </div>
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        ₹{{ formatPrice(item.price) }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {{ item.quantity }}
                      </td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        ₹{{ formatPrice(item.price * item.quantity) }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
          
          <!-- Order Summary -->
          <div class="border border-gray-200 rounded-lg p-4 mb-8">
            <h2 class="font-medium text-gray-900 mb-3 flex items-center">
              <Icon name="ph:receipt" class="h-5 w-5 mr-2 text-gray-500" />
              Order Summary
            </h2>
            <div class="text-sm">
              <div class="flex justify-between py-2 border-b border-gray-100">
                <span class="text-gray-600">Subtotal</span>
                <span class="text-gray-900 font-medium">₹{{ formatPrice(order.summary.subtotal) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-100">
                <span class="text-gray-600">Shipping</span>
                <span class="text-gray-900 font-medium">₹{{ formatPrice(order.summary.shipping) }}</span>
              </div>
              <div v-if="order.summary.discount" class="flex justify-between py-2 border-b border-gray-100">
                <span class="text-gray-600">Discount</span>
                <span class="text-green-600 font-medium">-₹{{ formatPrice(order.summary.discount) }}</span>
              </div>
              <div class="flex justify-between py-2 border-b border-gray-100">
                <span class="text-gray-600">Tax</span>
                <span class="text-gray-900 font-medium">₹{{ formatPrice(order.summary.tax) }}</span>
              </div>
              <div class="flex justify-between py-3 font-medium">
                <span class="text-gray-900">Total</span>
                <span class="text-deep-maroon text-lg">₹{{ formatPrice(order.summary.total) }}</span>
              </div>
            </div>
          </div>
          
          <!-- Tracking Information -->
          <div v-if="order.tracking" class="border border-gray-200 rounded-lg p-4 mb-8">
            <h2 class="font-medium text-gray-900 mb-3 flex items-center">
              <Icon name="ph:map-pin" class="h-5 w-5 mr-2 text-gray-500" />
              Tracking Information
            </h2>
            <div class="text-sm">
              <p class="mb-2">Tracking Number: <span class="font-medium text-gray-900">{{ order.tracking.number }}</span></p>
              <p class="mb-2">Carrier: <span class="font-medium text-gray-900">{{ order.tracking.carrier }}</span></p>
              <a :href="order.tracking.url" target="_blank" rel="noopener noreferrer" class="text-rose-gold hover:text-deep-maroon inline-flex items-center">
                Track Package
                <Icon name="ph:arrow-right" class="ml-1 h-4 w-4" />
              </a>
            </div>
          </div>
          
          <!-- Order Actions -->
          <div class="flex flex-wrap gap-4">
            <button 
              v-if="canCancel" 
              @click="cancelOrder" 
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold"
              :disabled="isCancelling"
            >
              <Icon v-if="isCancelling" name="ph:spinner" class="animate-spin -ml-1 mr-2 h-4 w-4 text-gray-500" />
              <Icon v-else name="ph:x-circle" class="-ml-1 mr-2 h-4 w-4 text-gray-500" />
              Cancel Order
            </button>
            
            <a 
              href="#" 
              @click.prevent="downloadInvoice" 
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold"
            >
              <Icon name="ph:download" class="-ml-1 mr-2 h-4 w-4 text-gray-500" />
              Download Invoice
            </a>
            
            <a 
              href="#" 
              @click.prevent="contactSupport" 
              class="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold"
            >
              <Icon name="ph:chat-circle-text" class="-ml-1 mr-2 h-4 w-4 text-gray-500" />
              Contact Support
            </a>
          </div>
        </div>
      </div>
      
      <!-- Back to Orders Link -->
      <div class="mt-6 text-center">
        <NuxtLink to="/dashboard/orders" class="text-rose-gold hover:text-deep-maroon transition-colors inline-flex items-center">
          <Icon name="ph:arrow-left" class="mr-1 h-4 w-4" />
          Back to Orders
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { format, parseISO, addDays } from 'date-fns';

// Get route params
const route = useRoute();
const orderId = route.params.id;

// SEO
useHead({
  title: `Order Details - Nakhrali Fashion`,
  meta: [
    {
      name: 'description',
      content: 'View your order details, tracking information, and order status.'
    }
  ]
});

// Auth
const { user } = useAuth();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const toast = useToast();

// Order data
const order = ref(null);
const isLoading = ref(true);
const error = ref(null);
const isCancelling = ref(false);

// Mock order data
const mockOrderData = {
  id: orderId,
  orderNumber: `NF-2023-00${orderId}`,
  status: ['Delivered', 'Processing', 'Shipped', 'Pending', 'Cancelled'][orderId % 5],
  date: new Date(2023, 5, 15 - (orderId % 15)).toISOString(),
  shipping: {
    name: 'Rahul Sharma',
    address: {
      line1: '123 Main Street',
      line2: 'Apartment 4B',
      city: 'Mumbai',
      state: 'Maharashtra',
      postalCode: '400001',
      country: 'India'
    },
    phone: '+91 98765 43210'
  },
  payment: {
    method: 'Credit Card',
    cardLast4: '4242',
    status: 'Paid',
    transactionId: `TXN${Math.random().toString(36).substring(2, 10).toUpperCase()}`
  },
  items: [
    {
      id: 1,
      name: 'Gold Plated Kundan Necklace Set',
      variant: 'Gold / Ruby',
      price: 8499,
      quantity: 1,
      image: 'https://via.placeholder.com/150/FFD700/000000?text=Necklace'
    },
    {
      id: 2,
      name: 'Pearl Embellished Jhumkas',
      variant: 'Silver',
      price: 2250,
      quantity: 2,
      image: 'https://via.placeholder.com/150/C0C0C0/000000?text=Jhumkas'
    }
  ],
  summary: {
    subtotal: 12999,
    shipping: 99,
    discount: orderId % 2 === 0 ? 500 : 0,
    tax: 650,
    total: 13248 - (orderId % 2 === 0 ? 500 : 0)
  },
  tracking: orderId % 5 === 0 || orderId % 5 === 2 ? {
    number: `TRK${Math.random().toString(36).substring(2, 10).toUpperCase()}`,
    carrier: 'BlueDart Express',
    url: 'https://www.bluedart.com/tracking'
  } : null
};

// Load order data
onMounted(async () => {
  isLoading.value = true;
  error.value = null;
  
  try {
    // In a real app, fetch from API
    // const response = await $fetch(`${apiBase}/orders/${orderId}`, {
    //   method: 'GET',
    //   headers: {
    //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    //   }
    // });
    // order.value = response;
    
    // Using mock data for demo
    setTimeout(() => {
      if (parseInt(orderId) > 0 && parseInt(orderId) <= 5) {
        order.value = mockOrderData;
      } else {
        error.value = 'The requested order could not be found. Please check the order number and try again.';
      }
      isLoading.value = false;
    }, 800);
  } catch (err) {
    console.error('Failed to load order:', err);
    error.value = 'Failed to load order details. Please try again later.';
    isLoading.value = false;
  }
});

// Format date
const formatDate = (dateString) => {
  try {
    return format(parseISO(dateString), 'MMMM d, yyyy');
  } catch (error) {
    return dateString;
  }
};

// Format price
const formatPrice = (price) => {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
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

// Check if order can be cancelled
const canCancel = computed(() => {
  if (!order.value) return false;
  
  const status = order.value.status.toLowerCase();
  return status === 'pending' || status === 'processing';
});

// Cancel order
const cancelOrder = async () => {
  if (!canCancel.value) return;
  
  isCancelling.value = true;
  
  try {
    // In a real app, call API
    // await $fetch(`${apiBase}/orders/${orderId}/cancel`, {
    //   method: 'POST',
    //   headers: {
    //     'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    //   }
    // });
    
    // Mock cancellation for demo
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    order.value.status = 'Cancelled';
    toast.success('Order has been cancelled successfully');
  } catch (err) {
    console.error('Failed to cancel order:', err);
    toast.error('Failed to cancel order. Please try again later.');
  } finally {
    isCancelling.value = false;
  }
};

// Download invoice
const downloadInvoice = () => {
  toast.info('Invoice download functionality will be implemented soon.');
};

// Contact support
const contactSupport = () => {
  toast.info('You will be redirected to our support page.');
  // In a real app, redirect to support page or open chat widget
};

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
});
</script>