<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Checkout</h1>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></div>
    </div>

    <!-- Error state -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
      {{ error }}
    </div>

    <!-- Empty cart -->
    <div v-else-if="!cartItems.length" class="text-center py-12">
      <div class="text-5xl mb-4">🛒</div>
      <h3 class="text-xl font-semibold mb-2">Your cart is empty</h3>
      <p class="text-gray-600 mb-6">Add items to your cart to proceed with checkout</p>
      <NuxtLink to="/products" class="bg-primary text-white px-6 py-2 rounded-md hover:bg-primary-dark transition">
        Browse Products
      </NuxtLink>
    </div>

    <!-- Checkout form -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Checkout form (2/3 width) -->
      <div class="lg:col-span-2">
        <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 class="text-xl font-semibold mb-4">Shipping Information</h2>
          
          <!-- Address selection -->
          <div v-if="savedAddresses.length > 0" class="mb-6">
            <label class="block text-gray-700 mb-2">Select a saved address</label>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div 
                v-for="address in savedAddresses" 
                :key="address.id"
                @click="selectAddress(address)"
                :class="[
                  'border rounded-lg p-4 cursor-pointer',
                  selectedAddress && selectedAddress.id === address.id 
                    ? 'border-primary bg-primary bg-opacity-5' 
                    : 'hover:border-gray-400'
                ]"
              >
                <div class="font-medium">{{ address.full_name }}</div>
                <div class="text-sm text-gray-600 mt-1">
                  {{ address.street_address }}, {{ address.city }}, {{ address.state }} {{ address.postal_code }}
                </div>
                <div class="text-sm text-gray-600 mt-1">{{ address.phone_number }}</div>
              </div>
            </div>
            <div class="mt-4">
              <button 
                @click="useNewAddress"
                class="text-primary hover:text-primary-dark text-sm font-medium"
              >
                + Add a new address
              </button>
            </div>
          </div>
          
          <!-- New address form -->
          <div v-if="!selectedAddress || isAddingNewAddress">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label for="full_name" class="block text-gray-700 mb-1">Full Name</label>
                <input 
                  id="full_name"
                  v-model="shippingAddress.full_name"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  required
                >
              </div>
              <div>
                <label for="phone_number" class="block text-gray-700 mb-1">Phone Number</label>
                <input 
                  id="phone_number"
                  v-model="shippingAddress.phone_number"
                  type="tel"
                  class="w-full px-3 py-2 border rounded-md"
                  required
                >
              </div>
            </div>
            
            <div class="mb-4">
              <label for="street_address" class="block text-gray-700 mb-1">Street Address</label>
              <input 
                id="street_address"
                v-model="shippingAddress.street_address"
                type="text"
                class="w-full px-3 py-2 border rounded-md"
                required
              >
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label for="city" class="block text-gray-700 mb-1">City</label>
                <input 
                  id="city"
                  v-model="shippingAddress.city"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  required
                >
              </div>
              <div>
                <label for="state" class="block text-gray-700 mb-1">State</label>
                <input 
                  id="state"
                  v-model="shippingAddress.state"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  required
                >
              </div>
              <div>
                <label for="postal_code" class="block text-gray-700 mb-1">Postal Code</label>
                <input 
                  id="postal_code"
                  v-model="shippingAddress.postal_code"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  required
                >
              </div>
            </div>
            
            <div class="mb-4">
              <label for="country" class="block text-gray-700 mb-1">Country</label>
              <select 
                id="country"
                v-model="shippingAddress.country"
                class="w-full px-3 py-2 border rounded-md"
                required
              >
                <option value="India">India</option>
                <option value="United States">United States</option>
                <option value="United Kingdom">United Kingdom</option>
                <!-- Add more countries as needed -->
              </select>
            </div>
            
            <div class="mb-4">
              <label class="flex items-center">
                <input 
                  type="checkbox"
                  v-model="saveAddress"
                  class="mr-2"
                >
                <span class="text-sm text-gray-700">Save this address for future orders</span>
              </label>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
          <h2 class="text-xl font-semibold mb-4">Shipping Method</h2>
          
          <div class="space-y-3">
            <label 
              v-for="method in shippingMethods" 
              :key="method.id"
              class="flex items-start p-3 border rounded-md cursor-pointer"
              :class="selectedShippingMethod === method.id ? 'border-primary bg-primary bg-opacity-5' : 'hover:border-gray-400'"
            >
              <input 
                type="radio"
                :value="method.id"
                v-model="selectedShippingMethod"
                class="mt-1 mr-3"
              >
              <div class="flex-1">
                <div class="font-medium">{{ method.name }}</div>
                <div class="text-sm text-gray-600">{{ method.description }}</div>
              </div>
              <div class="font-medium">
                {{ formatPrice(method.price) }}
              </div>
            </label>
          </div>
        </div>
        
        <div class="bg-white rounded-lg shadow-sm p-6">
          <h2 class="text-xl font-semibold mb-4">Payment Method</h2>
          
          <div class="space-y-3">
            <label 
              v-for="method in paymentMethods" 
              :key="method.id"
              class="flex items-center p-3 border rounded-md cursor-pointer"
              :class="selectedPaymentMethod === method.id ? 'border-primary bg-primary bg-opacity-5' : 'hover:border-gray-400'"
            >
              <input 
                type="radio"
                :value="method.id"
                v-model="selectedPaymentMethod"
                class="mr-3"
              >
              <div class="flex-1">
                <div class="font-medium">{{ method.name }}</div>
              </div>
              <div class="w-12 h-8 flex items-center justify-center">
                <img v-if="method.icon" :src="method.icon" :alt="method.name" class="max-h-full">
              </div>
            </label>
          </div>
          
          <!-- Credit Card Form (if credit card is selected) -->
          <div v-if="selectedPaymentMethod === 'credit_card'" class="mt-6 p-4 border rounded-md">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label for="card_number" class="block text-gray-700 mb-1">Card Number</label>
                <input 
                  id="card_number"
                  v-model="paymentDetails.card_number"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  placeholder="1234 5678 9012 3456"
                  required
                >
              </div>
              <div>
                <label for="card_name" class="block text-gray-700 mb-1">Name on Card</label>
                <input 
                  id="card_name"
                  v-model="paymentDetails.card_name"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  required
                >
              </div>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div>
                <label for="expiry" class="block text-gray-700 mb-1">Expiry Date</label>
                <input 
                  id="expiry"
                  v-model="paymentDetails.expiry"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  placeholder="MM/YY"
                  required
                >
              </div>
              <div>
                <label for="cvv" class="block text-gray-700 mb-1">CVV</label>
                <input 
                  id="cvv"
                  v-model="paymentDetails.cvv"
                  type="text"
                  class="w-full px-3 py-2 border rounded-md"
                  placeholder="123"
                  required
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Order summary (1/3 width) -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow-sm p-6 sticky top-6">
          <h2 class="text-xl font-semibold mb-4">Order Summary</h2>
          
          <div class="max-h-80 overflow-y-auto mb-4">
            <div 
              v-for="item in cartItems" 
              :key="item.id"
              class="flex py-3 border-b last:border-b-0"
            >
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
          
          <!-- Coupon code -->
          <div class="mb-4">
            <div class="flex">
              <input 
                v-model="couponCode"
                type="text"
                placeholder="Coupon code"
                class="flex-1 px-3 py-2 border rounded-l-md"
              >
              <button 
                @click="applyCoupon"
                class="bg-gray-200 hover:bg-gray-300 px-4 py-2 rounded-r-md"
                :disabled="isApplyingCoupon"
              >
                Apply
              </button>
            </div>
            <div v-if="couponError" class="text-red-600 text-sm mt-1">
              {{ couponError }}
            </div>
            <div v-if="appliedCoupon" class="text-green-600 text-sm mt-1">
              Coupon applied: {{ appliedCoupon.code }} ({{ appliedCoupon.discount_type === 'percentage' ? appliedCoupon.discount_value + '%' : formatPrice(appliedCoupon.discount_value) }} off)
            </div>
          </div>
          
          <!-- Price breakdown -->
          <div class="space-y-2 mb-4">
            <div class="flex justify-between">
              <span class="text-gray-600">Subtotal</span>
              <span>{{ formatPrice(cartTotal) }}</span>
            </div>
            <div v-if="appliedCoupon" class="flex justify-between text-green-600">
              <span>Discount</span>
              <span>-{{ formatPrice(discountAmount) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Shipping</span>
              <span>{{ selectedShippingMethod ? formatPrice(getShippingPrice()) : 'Select shipping method' }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-gray-600">Tax</span>
              <span>{{ formatPrice(calculateTax()) }}</span>
            </div>
            <div class="flex justify-between font-bold text-lg pt-2 border-t">
              <span>Total</span>
              <span>{{ formatPrice(calculateTotal()) }}</span>
            </div>
          </div>
          
          <!-- Place order button -->
          <button 
            @click="placeOrder"
            class="w-full bg-primary text-white py-3 rounded-md hover:bg-primary-dark transition"
            :disabled="isProcessingOrder || !isFormValid"
          >
            <span v-if="isProcessingOrder">Processing...</span>
            <span v-else>Place Order</span>
          </button>
          
          <div v-if="!isFormValid" class="text-red-600 text-sm mt-2">
            Please fill in all required fields
          </div>
          
          <div class="text-sm text-gray-500 mt-4">
            By placing your order, you agree to our
            <NuxtLink to="/terms" class="text-primary hover:underline">Terms of Service</NuxtLink> and
            <NuxtLink to="/privacy" class="text-primary hover:underline">Privacy Policy</NuxtLink>.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useCart } from '~/composables/useCart'
import { useAuth } from '~/composables/useAuth'

const router = useRouter()
const toast = useToast()
const config = useRuntimeConfig()
const { isAuthenticated, user, accessToken } = useAuth()
const { 
  cartItems, 
  cartTotal, 
  isLoading: isCartLoading, 
  error: cartError,
  clearCart
} = useCart()

// Load Razorpay script
onMounted(() => {
  // Load Razorpay script if not already loaded
  if (process.client && !window.Razorpay) {
    const script = document.createElement('script')
    script.src = 'https://checkout.razorpay.com/v1/checkout.js'
    script.async = true
    document.body.appendChild(script)
  }
})

// Redirect if not authenticated
onMounted(() => {
  if (!isAuthenticated.value) {
    toast.error('Please log in to proceed with checkout')
    router.push('/login?redirect=/checkout')
  }
})

// State
const isLoading = computed(() => isCartLoading.value)
const error = computed(() => cartError.value)
const savedAddresses = ref([])
const selectedAddress = ref(null)
const isAddingNewAddress = ref(false)
const saveAddress = ref(true)
const shippingAddress = ref({
  full_name: '',
  phone_number: '',
  street_address: '',
  city: '',
  state: '',
  postal_code: '',
  country: 'India'
})

// Shipping methods
const shippingMethods = ref([
  {
    id: 'standard',
    name: 'Standard Shipping',
    description: 'Delivery in 5-7 business days',
    price: 99
  },
  {
    id: 'express',
    name: 'Express Shipping',
    description: 'Delivery in 2-3 business days',
    price: 199
  },
  {
    id: 'same_day',
    name: 'Same Day Delivery',
    description: 'Available only in select cities',
    price: 299
  }
])
const selectedShippingMethod = ref('standard')

// Payment methods
const paymentMethods = ref([
  {
    id: 'credit_card',
    name: 'Credit/Debit Card',
    icon: '/images/payment/card.svg'
  },
  {
    id: 'upi',
    name: 'UPI',
    icon: '/images/payment/upi.svg'
  },
  {
    id: 'cod',
    name: 'Cash on Delivery',
    icon: '/images/payment/cod.svg'
  }
])
const selectedPaymentMethod = ref('credit_card')
const paymentDetails = ref({
  card_number: '',
  card_name: '',
  expiry: '',
  cvv: ''
})

// Coupon
const couponCode = ref('')
const appliedCoupon = ref(null)
const couponError = ref('')
const isApplyingCoupon = ref(false)

// Order processing
const isProcessingOrder = ref(false)

// Load user addresses
onMounted(async () => {
  if (isAuthenticated.value) {
    await loadUserAddresses()
  }
})

// Watch for user changes
watch(user, async () => {
  if (user.value) {
    await loadUserAddresses()
  }
})

// Load user's saved addresses
const loadUserAddresses = async () => {
  try {
    // This would be an API call in a real application
    // For now, we'll use mock data
    savedAddresses.value = [
      {
        id: '1',
        full_name: 'John Doe',
        phone_number: '+91 9876543210',
        street_address: '123 Main Street',
        city: 'Mumbai',
        state: 'Maharashtra',
        postal_code: '400001',
        country: 'India'
      },
      {
        id: '2',
        full_name: 'John Doe',
        phone_number: '+91 9876543210',
        street_address: '456 Park Avenue',
        city: 'Delhi',
        state: 'Delhi',
        postal_code: '110001',
        country: 'India'
      }
    ]
    
    // Select the first address by default if available
    if (savedAddresses.value.length > 0) {
      selectedAddress.value = savedAddresses.value[0]
      // Copy to shipping address
      Object.assign(shippingAddress.value, savedAddresses.value[0])
    }
  } catch (err) {
    console.error('Error loading addresses:', err)
    toast.error('Failed to load your saved addresses')
  }
}

// Select a saved address
const selectAddress = (address) => {
  selectedAddress.value = address
  isAddingNewAddress.value = false
  // Copy to shipping address
  Object.assign(shippingAddress.value, address)
}

// Use a new address
const useNewAddress = () => {
  selectedAddress.value = null
  isAddingNewAddress.value = true
  // Reset shipping address
  shippingAddress.value = {
    full_name: '',
    phone_number: '',
    street_address: '',
    city: '',
    state: '',
    postal_code: '',
    country: 'India'
  }
}

// Apply coupon
const applyCoupon = async () => {
  if (!couponCode.value) return
  
  isApplyingCoupon.value = true
  couponError.value = ''
  
  try {
    // This would be an API call in a real application
    // For now, we'll use mock data
    const mockCoupons = {
      'WELCOME10': {
        code: 'WELCOME10',
        discount_type: 'percentage',
        discount_value: 10,
        min_order_value: 1000
      },
      'FLAT200': {
        code: 'FLAT200',
        discount_type: 'fixed',
        discount_value: 200,
        min_order_value: 2000
      }
    }
    
    const coupon = mockCoupons[couponCode.value.toUpperCase()]
    
    if (!coupon) {
      couponError.value = 'Invalid coupon code'
      return
    }
    
    if (cartTotal.value < coupon.min_order_value) {
      couponError.value = `This coupon requires a minimum order of ${formatPrice(coupon.min_order_value)}`
      return
    }
    
    appliedCoupon.value = coupon
    toast.success('Coupon applied successfully')
  } catch (err) {
    console.error('Error applying coupon:', err)
    couponError.value = 'Failed to apply coupon'
  } finally {
    isApplyingCoupon.value = false
  }
}

// Calculate discount amount
const discountAmount = computed(() => {
  if (!appliedCoupon.value) return 0
  
  if (appliedCoupon.value.discount_type === 'percentage') {
    return (cartTotal.value * appliedCoupon.value.discount_value) / 100
  } else {
    return Math.min(appliedCoupon.value.discount_value, cartTotal.value)
  }
})

// Get shipping price
const getShippingPrice = () => {
  const method = shippingMethods.value.find(m => m.id === selectedShippingMethod.value)
  return method ? method.price : 0
}

// Calculate tax (assuming 18% GST)
const calculateTax = () => {
  const subtotalAfterDiscount = cartTotal.value - discountAmount.value
  return subtotalAfterDiscount * 0.18
}

// Calculate total
const calculateTotal = () => {
  const subtotal = cartTotal.value
  const discount = discountAmount.value
  const shipping = getShippingPrice()
  const tax = calculateTax()
  
  return subtotal - discount + shipping + tax
}

// Check if form is valid
const isFormValid = computed(() => {
  // Check shipping address
  const addressValid = (
    selectedAddress.value || (
      shippingAddress.value.full_name &&
      shippingAddress.value.phone_number &&
      shippingAddress.value.street_address &&
      shippingAddress.value.city &&
      shippingAddress.value.state &&
      shippingAddress.value.postal_code
    )
  )
  
  // Check shipping method
  const shippingValid = !!selectedShippingMethod.value
  
  // Check payment method
  let paymentValid = !!selectedPaymentMethod.value
  
  // Additional validation for credit card
  if (selectedPaymentMethod.value === 'credit_card') {
    paymentValid = paymentValid && (
      paymentDetails.value.card_number &&
      paymentDetails.value.card_name &&
      paymentDetails.value.expiry &&
      paymentDetails.value.cvv
    )
  }
  
  return addressValid && shippingValid && paymentValid && cartItems.value.length > 0
})

// Place order
const placeOrder = async () => {
  if (!isFormValid.value) {
    toast.error('Please fill in all required fields')
    return
  }
  
  isProcessingOrder.value = true
  
  try {
    // Prepare order data
    const orderData = {
      items: cartItems.value.map(item => ({
        product_id: item.product.id,
        variant_id: item.variant?.id,
        quantity: item.quantity,
        price: item.price
      })),
      shipping_address: selectedAddress.value || shippingAddress.value,
      shipping_method: selectedShippingMethod.value,
      payment_method: selectedPaymentMethod.value,
      payment_details: selectedPaymentMethod.value === 'credit_card' ? paymentDetails.value : null,
      coupon_code: appliedCoupon.value?.code,
      subtotal: cartTotal.value,
      discount: discountAmount.value,
      shipping: getShippingPrice(),
      tax: calculateTax(),
      total: calculateTotal()
    }
    
    // Save new address if needed
    if (saveAddress.value && isAddingNewAddress.value) {
      try {
        // This would be an API call in a real application
        const response = await $fetch(`${config.public.apiBase}/user/addresses`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${accessToken.value}`
          },
          body: shippingAddress.value
        })
        
        // Update the selected address with the saved one
        if (response.id) {
          selectedAddress.value = response
        }
      } catch (addressErr) {
        console.error('Error saving address:', addressErr)
        // Continue with order even if address saving fails
      }
    }
    
    // Handle different payment methods
    if (selectedPaymentMethod.value === 'credit_card' || selectedPaymentMethod.value === 'upi') {
      // Create order in backend first
      const orderResponse = await $fetch(`${config.public.apiBase}/orders`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: orderData
      })
      
      if (orderResponse.id) {
        // Initialize Razorpay payment
        const razorpayOptions = {
          key: config.public.razorpayKey, // From your Razorpay Dashboard
          amount: calculateTotal() * 100, // Amount in smallest currency unit (paise)
          currency: 'INR',
          name: 'Nakhrali Fashion',
          description: 'Jewelry Purchase',
          order_id: orderResponse.razorpay_order_id,
          image: '/images/logo.png',
          handler: async function (response) {
            // Verify payment with backend
            try {
              await $fetch(`${config.public.apiBase}/orders/${orderResponse.id}/verify-payment`, {
                method: 'POST',
                headers: {
                  'Authorization': `Bearer ${accessToken.value}`
                },
                body: {
                  razorpay_payment_id: response.razorpay_payment_id,
                  razorpay_order_id: response.razorpay_order_id,
                  razorpay_signature: response.razorpay_signature
                }
              })
              
              // Clear cart after successful payment
              await clearCart()
              
              // Redirect to order confirmation
              router.push(`/order-confirmation?id=${orderResponse.id}`)
              
              toast.success('Payment successful! Your order has been placed.')
            } catch (verifyErr) {
              console.error('Payment verification failed:', verifyErr)
              toast.error('Payment verification failed. Please contact support.')
            }
          },
          prefill: {
            name: user.value?.first_name + ' ' + user.value?.last_name,
            email: user.value?.email,
            contact: shippingAddress.value.phone_number
          },
          theme: {
            color: '#8B0000' // Deep Maroon color
          },
          modal: {
            ondismiss: function() {
              isProcessingOrder.value = false
              toast.info('Payment cancelled. You can try again later.')
            }
          }
        }
        
        // Open Razorpay payment form
        const razorpay = new window.Razorpay(razorpayOptions)
        razorpay.open()
      }
    } else if (selectedPaymentMethod.value === 'cod') {
      // For Cash on Delivery, create order directly
      const orderResponse = await $fetch(`${config.public.apiBase}/orders`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: {
          ...orderData,
          payment_status: 'pending'
        }
      })
      
      if (orderResponse.id) {
        // Clear cart
        await clearCart()
        
        // Redirect to order confirmation
        router.push(`/order-confirmation?id=${orderResponse.id}`)
        
        toast.success('Order placed successfully! You will pay on delivery.')
      }
    }
  } catch (err) {
    console.error('Error placing order:', err)
    toast.error('Failed to place order. Please try again.')
  } finally {
    isProcessingOrder.value = false
  }
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