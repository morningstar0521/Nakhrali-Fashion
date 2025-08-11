<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">Order Management</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Track and manage customer orders</p>
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
              placeholder="Search orders..."
              class="pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              @input="handleSearch"
            />
            <div class="absolute left-3 top-2.5">
              <Icon name="ph:magnifying-glass" class="h-5 w-5 text-gray-400 dark:text-gray-500" />
            </div>
          </div>

          <select
            v-model="filters.status"
            class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Status</option>
            <option value="placed">Placed</option>
            <option value="confirmed">Confirmed</option>
            <option value="processing">Processing</option>
            <option value="shipped">Shipped</option>
            <option value="delivered">Delivered</option>
            <option value="cancelled">Cancelled</option>
          </select>

          <select
            v-model="filters.timeframe"
            class="px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
          >
            <option value="">All Time</option>
            <option value="today">Today</option>
            <option value="yesterday">Yesterday</option>
            <option value="last7days">Last 7 Days</option>
            <option value="last30days">Last 30 Days</option>
            <option value="thisMonth">This Month</option>
            <option value="lastMonth">Last Month</option>
          </select>
        </div>

        <div class="flex space-x-2">
          <button
            @click="exportOrders"
            class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center justify-center transition-colors"
          >
            <Icon name="ph:download" class="mr-2 h-5 w-5" />
            Export
          </button>
          <button
            @click="printOrders"
            class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 flex items-center justify-center transition-colors"
          >
            <Icon name="ph:printer" class="mr-2 h-5 w-5" />
            Print
          </button>
        </div>
      </div>

      <!-- Orders Table -->
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
        <div class="overflow-x-auto">
          <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead>
              <tr>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Order #</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Customer</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Date</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Status</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Items</th>
                <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Total</th>
                <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody class="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              <tr v-for="order in paginatedOrders" :key="order.id" class="hover:bg-gray-50 dark:hover:bg-gray-700">
                <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">{{ order.orderNumber }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ order.customerName }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ formatDate(order.date) }}</td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusClass(order.status)">
                    {{ order.status }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">{{ order.items }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">₹{{ order.total }}</td>
                <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button @click="viewOrder(order)" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 mr-2">
                    <Icon name="ph:eye" class="h-5 w-5" />
                  </button>
                  <button @click="updateOrderStatus(order)" class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80">
                    <Icon name="ph:pencil-simple" class="h-5 w-5" />
                  </button>
                </td>
              </tr>
              <tr v-if="paginatedOrders.length === 0">
                <td colspan="7" class="px-6 py-4 text-center text-gray-500 dark:text-gray-400">
                  No orders found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <!-- Pagination -->
        <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <div class="text-sm text-gray-500 dark:text-gray-400">
            Showing <span class="font-medium">{{ paginationStart }}</span> to <span class="font-medium">{{ paginationEnd }}</span> of <span class="font-medium">{{ totalOrders }}</span> orders
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
              :disabled="paginationEnd >= totalOrders" 
              class="px-3 py-1 rounded-md border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Next
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- View Order Modal -->
    <div v-if="showOrderModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h3 class="text-xl font-display text-deep-maroon dark:text-rose-gold">
            Order Details - {{ selectedOrder?.orderNumber }}
          </h3>
          <button @click="showOrderModal = false" class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
            <Icon name="ph:x" class="h-5 w-5" />
          </button>
        </div>
        <div class="p-6" v-if="selectedOrder">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-2">Order Information</h4>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div class="grid grid-cols-2 gap-4">
                  <div>
                    <p class="text-xs text-gray-500 dark:text-gray-400">Order Number</p>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedOrder.orderNumber }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500 dark:text-gray-400">Date</p>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ formatDate(selectedOrder.date) }}</p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500 dark:text-gray-400">Status</p>
                    <p class="text-sm font-medium">
                      <span class="px-2 py-0.5 inline-flex text-xs leading-5 font-semibold rounded-full" :class="getStatusClass(selectedOrder.status)">
                        {{ selectedOrder.status }}
                      </span>
                    </p>
                  </div>
                  <div>
                    <p class="text-xs text-gray-500 dark:text-gray-400">Payment Method</p>
                    <p class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedOrder.paymentMethod }}</p>
                  </div>
                </div>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-2">Customer Information</h4>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div class="mb-3">
                  <p class="text-xs text-gray-500 dark:text-gray-400">Name</p>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedOrder.customerName }}</p>
                </div>
                <div class="mb-3">
                  <p class="text-xs text-gray-500 dark:text-gray-400">Email</p>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedOrder.customerEmail }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 dark:text-gray-400">Phone</p>
                  <p class="text-sm font-medium text-gray-900 dark:text-white">{{ selectedOrder.customerPhone }}</p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-2">Shipping Address</h4>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <p class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.shippingAddress.line1 }}</p>
                <p v-if="selectedOrder.shippingAddress.line2" class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.shippingAddress.line2 }}</p>
                <p class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.shippingAddress.city }}, {{ selectedOrder.shippingAddress.state }} {{ selectedOrder.shippingAddress.postalCode }}</p>
                <p class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.shippingAddress.country }}</p>
              </div>
            </div>
            
            <div>
              <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-2">Billing Address</h4>
              <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <p class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.billingAddress.line1 }}</p>
                <p v-if="selectedOrder.billingAddress.line2" class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.billingAddress.line2 }}</p>
                <p class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.billingAddress.city }}, {{ selectedOrder.billingAddress.state }} {{ selectedOrder.billingAddress.postalCode }}</p>
                <p class="text-sm text-gray-900 dark:text-white">{{ selectedOrder.billingAddress.country }}</p>
              </div>
            </div>
          </div>
          
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 uppercase mb-2">Order Items</h4>
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg overflow-hidden mb-6">
            <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-600">
              <thead>
                <tr>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Product</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Price</th>
                  <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Quantity</th>
                  <th class="px-4 py-3 text-right text-xs font-medium text-gray-500 dark:text-gray-400 uppercase">Total</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-200 dark:divide-gray-600">
                <tr v-for="(item, index) in selectedOrder.items" :key="index">
                  <td class="px-4 py-3">
                    <div class="flex items-center">
                      <div class="h-10 w-10 flex-shrink-0 rounded overflow-hidden bg-gray-200 dark:bg-gray-600">
                        <img v-if="item.image" :src="item.image" :alt="item.name" class="h-10 w-10 object-cover" />
                        <div v-else class="h-10 w-10 flex items-center justify-center text-gray-500 dark:text-gray-400">
                          <Icon name="ph:image" class="h-5 w-5" />
                        </div>
                      </div>
                      <div class="ml-4">
                        <p class="text-sm font-medium text-gray-900 dark:text-white">{{ item.name }}</p>
                        <p v-if="item.variant" class="text-xs text-gray-500 dark:text-gray-400">{{ item.variant }}</p>
                      </div>
                    </div>
                  </td>
                  <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">₹{{ item.price }}</td>
                  <td class="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">{{ item.quantity }}</td>
                  <td class="px-4 py-3 text-sm text-gray-900 dark:text-white text-right">₹{{ item.price * item.quantity }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
            <div class="flex justify-between py-1">
              <span class="text-sm text-gray-500 dark:text-gray-400">Subtotal</span>
              <span class="text-sm text-gray-900 dark:text-white">₹{{ selectedOrder.subtotal }}</span>
            </div>
            <div class="flex justify-between py-1">
              <span class="text-sm text-gray-500 dark:text-gray-400">Shipping</span>
              <span class="text-sm text-gray-900 dark:text-white">₹{{ selectedOrder.shipping }}</span>
            </div>
            <div class="flex justify-between py-1">
              <span class="text-sm text-gray-500 dark:text-gray-400">Tax</span>
              <span class="text-sm text-gray-900 dark:text-white">₹{{ selectedOrder.tax }}</span>
            </div>
            <div class="flex justify-between py-1 border-t border-gray-200 dark:border-gray-600 mt-2 pt-2">
              <span class="text-base font-medium text-gray-900 dark:text-white">Total</span>
              <span class="text-base font-medium text-gray-900 dark:text-white">₹{{ selectedOrder.total }}</span>
            </div>
          </div>
          
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              @click="showOrderModal = false" 
              class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Close
            </button>
            <button 
              @click="updateOrderStatus(selectedOrder)" 
              class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg"
            >
              Update Status
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Update Status Modal -->
    <div v-if="showStatusModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full">
        <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-xl font-display text-deep-maroon dark:text-rose-gold">Update Order Status</h3>
        </div>
        <div class="p-6">
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Order Number</label>
            <p class="text-gray-900 dark:text-white font-medium">{{ selectedOrder?.orderNumber }}</p>
          </div>
          
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Status</label>
            <select 
              v-model="statusForm.status" 
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
            >
              <option value="placed">Placed</option>
              <option value="confirmed">Confirmed</option>
              <option value="processing">Processing</option>
              <option value="shipped">Shipped</option>
              <option value="delivered">Delivered</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>
          
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Notes (Optional)</label>
            <textarea 
              v-model="statusForm.notes" 
              rows="3"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
              placeholder="Add notes about this status change"
            ></textarea>
          </div>
          
          <div class="flex justify-end space-x-3">
            <button 
              @click="showStatusModal = false" 
              class="px-4 py-2 border border-gray-300 dark:border-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700"
            >
              Cancel
            </button>
            <button 
              @click="saveOrderStatus()" 
              class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg"
            >
              Save Changes
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
  title: 'Order Management - Nakhrali Fashion Admin',
  meta: [
    {
      name: 'description',
      content: 'Manage customer orders for Nakhrali Fashion.'
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
  status: '',
  timeframe: ''
})
const currentPage = ref(1)
const itemsPerPage = 10
const showOrderModal = ref(false)
const showStatusModal = ref(false)
const selectedOrder = ref(null)
const statusForm = ref({
  status: '',
  notes: ''
})

// Mock data for orders
const orders = ref([
  {
    id: '1',
    orderNumber: 'NK20230501123456',
    customerName: 'Priya Sharma',
    customerEmail: 'priya@example.com',
    customerPhone: '+91 98765 43210',
    date: '2023-05-01',
    status: 'delivered',
    items: 3,
    total: '12,499',
    subtotal: '11,999',
    shipping: '0',
    tax: '500',
    paymentMethod: 'Credit Card',
    shippingAddress: {
      line1: '123 Main Street',
      line2: 'Apartment 4B',
      city: 'Mumbai',
      state: 'Maharashtra',
      postalCode: '400001',
      country: 'India'
    },
    billingAddress: {
      line1: '123 Main Street',
      line2: 'Apartment 4B',
      city: 'Mumbai',
      state: 'Maharashtra',
      postalCode: '400001',
      country: 'India'
    },
    items: [
      {
        name: 'Elegant Pearl Necklace',
        variant: 'Gold',
        price: 4999,
        quantity: 1,
        image: 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      },
      {
        name: 'Diamond Stud Earrings',
        variant: 'White Gold',
        price: 3500,
        quantity: 2,
        image: 'https://images.unsplash.com/photo-1629224316810-9d8805b95e76?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      }
    ]
  },
  {
    id: '2',
    orderNumber: 'NK20230502123457',
    customerName: 'Rahul Patel',
    customerEmail: 'rahul@example.com',
    customerPhone: '+91 87654 32109',
    date: '2023-05-02',
    status: 'shipped',
    items: 2,
    total: '8,999',
    subtotal: '8,499',
    shipping: '0',
    tax: '500',
    paymentMethod: 'UPI',
    shippingAddress: {
      line1: '456 Park Avenue',
      line2: '',
      city: 'Delhi',
      state: 'Delhi',
      postalCode: '110001',
      country: 'India'
    },
    billingAddress: {
      line1: '456 Park Avenue',
      line2: '',
      city: 'Delhi',
      state: 'Delhi',
      postalCode: '110001',
      country: 'India'
    },
    items: [
      {
        name: 'Gold Chain Bracelet',
        variant: 'Yellow Gold',
        price: 6499,
        quantity: 1,
        image: 'https://images.unsplash.com/photo-1611652022419-a9419f74343d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      },
      {
        name: 'Silver Anklet with Bells',
        variant: 'Silver',
        price: 2000,
        quantity: 1,
        image: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      }
    ]
  },
  {
    id: '3',
    orderNumber: 'NK20230503123458',
    customerName: 'Ananya Singh',
    customerEmail: 'ananya@example.com',
    customerPhone: '+91 76543 21098',
    date: '2023-05-03',
    status: 'processing',
    items: 1,
    total: '15,999',
    subtotal: '15,499',
    shipping: '0',
    tax: '500',
    paymentMethod: 'Net Banking',
    shippingAddress: {
      line1: '789 Lake View',
      line2: 'Floor 3',
      city: 'Bangalore',
      state: 'Karnataka',
      postalCode: '560001',
      country: 'India'
    },
    billingAddress: {
      line1: '789 Lake View',
      line2: 'Floor 3',
      city: 'Bangalore',
      state: 'Karnataka',
      postalCode: '560001',
      country: 'India'
    },
    items: [
      {
        name: 'Ruby Pendant Necklace',
        variant: 'Rose Gold',
        price: 15499,
        quantity: 1,
        image: 'https://images.unsplash.com/photo-1602173574767-37ac01994b2a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      }
    ]
  },
  {
    id: '4',
    orderNumber: 'NK20230504123459',
    customerName: 'Vikram Malhotra',
    customerEmail: 'vikram@example.com',
    customerPhone: '+91 65432 10987',
    date: '2023-05-04',
    status: 'placed',
    items: 2,
    total: '6,499',
    subtotal: '5,999',
    shipping: '0',
    tax: '500',
    paymentMethod: 'Cash on Delivery',
    shippingAddress: {
      line1: '321 River Road',
      line2: '',
      city: 'Kolkata',
      state: 'West Bengal',
      postalCode: '700001',
      country: 'India'
    },
    billingAddress: {
      line1: '321 River Road',
      line2: '',
      city: 'Kolkata',
      state: 'West Bengal',
      postalCode: '700001',
      country: 'India'
    },
    items: [
      {
        name: 'Silver Anklet with Bells',
        variant: 'Silver',
        price: 2000,
        quantity: 2,
        image: 'https://images.unsplash.com/photo-1535632066927-ab7c9ab60908?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      },
      {
        name: 'Platinum Wedding Band',
        variant: 'Platinum',
        price: 1999,
        quantity: 1,
        image: 'https://images.unsplash.com/photo-1586104195538-050b9f9b589c?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      }
    ]
  },
  {
    id: '5',
    orderNumber: 'NK20230505123460',
    customerName: 'Neha Gupta',
    customerEmail: 'neha@example.com',
    customerPhone: '+91 54321 09876',
    date: '2023-05-05',
    status: 'confirmed',
    items: 1,
    total: '9,999',
    subtotal: '9,499',
    shipping: '0',
    tax: '500',
    paymentMethod: 'Debit Card',
    shippingAddress: {
      line1: '654 Hill View',
      line2: 'Apartment 7C',
      city: 'Chennai',
      state: 'Tamil Nadu',
      postalCode: '600001',
      country: 'India'
    },
    billingAddress: {
      line1: '654 Hill View',
      line2: 'Apartment 7C',
      city: 'Chennai',
      state: 'Tamil Nadu',
      postalCode: '600001',
      country: 'India'
    },
    items: [
      {
        name: 'Sapphire Engagement Ring',
        variant: 'White Gold',
        price: 9499,
        quantity: 1,
        image: 'https://images.unsplash.com/photo-1605100804763-247f67b3557e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800&q=80'
      }
    ]
  }
])

// Computed properties
const filteredOrders = computed(() => {
  let result = [...orders.value]
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(order => 
      order.orderNumber.toLowerCase().includes(query) || 
      order.customerName.toLowerCase().includes(query) ||
      order.customerEmail.toLowerCase().includes(query)
    )
  }
  
  // Apply status filter
  if (filters.value.status) {
    result = result.filter(order => order.status === filters.value.status)
  }
  
  // Apply timeframe filter
  if (filters.value.timeframe) {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
    
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)
    
    const last7Days = new Date(today)
    last7Days.setDate(last7Days.getDate() - 7)
    
    const last30Days = new Date(today)
    last30Days.setDate(last30Days.getDate() - 30)
    
    const thisMonth = new Date(today.getFullYear(), today.getMonth(), 1)
    
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1)
    const lastMonthEnd = new Date(today.getFullYear(), today.getMonth(), 0)
    
    result = result.filter(order => {
      const orderDate = new Date(order.date)
      orderDate.setHours(0, 0, 0, 0)
      
      switch (filters.value.timeframe) {
        case 'today':
          return orderDate.getTime() === today.getTime()
        case 'yesterday':
          return orderDate.getTime() === yesterday.getTime()
        case 'last7days':
          return orderDate >= last7Days
        case 'last30days':
          return orderDate >= last30Days
        case 'thisMonth':
          return orderDate >= thisMonth
        case 'lastMonth':
          return orderDate >= lastMonth && orderDate <= lastMonthEnd
        default:
          return true
      }
    })
  }
  
  return result
})

const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredOrders.value.slice(start, end)
})

const totalOrders = computed(() => filteredOrders.value.length)

const paginationStart = computed(() => {
  if (totalOrders.value === 0) return 0
  return (currentPage.value - 1) * itemsPerPage + 1
})

const paginationEnd = computed(() => {
  return Math.min(currentPage.value * itemsPerPage, totalOrders.value)
})

// Methods
const handleSearch = () => {
  currentPage.value = 1 // Reset to first page on search
}

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

const viewOrder = (order) => {
  selectedOrder.value = order
  showOrderModal.value = true
}

const updateOrderStatus = (order) => {
  selectedOrder.value = order
  statusForm.value.status = order.status
  statusForm.value.notes = ''
  showStatusModal.value = true
}

const saveOrderStatus = () => {
  // In a real application, this would be an API call
  if (selectedOrder.value) {
    const index = orders.value.findIndex(o => o.id === selectedOrder.value.id)
    if (index !== -1) {
      orders.value[index].status = statusForm.value.status
      selectedOrder.value.status = statusForm.value.status
    }
  }
  showStatusModal.value = false
}

const exportOrders = () => {
  // In a real application, this would generate a CSV or Excel file
  alert('Export functionality would be implemented here')
}

const printOrders = () => {
  // In a real application, this would open a print dialog
  window.print()
}
</script>