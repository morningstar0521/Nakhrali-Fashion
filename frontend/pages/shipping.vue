<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 class="text-3xl font-display font-bold text-deep-maroon mb-8">Shipping Information</h1>
      
      <div class="space-y-8">
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Shipping Options</h2>
          
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Shipping Method</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Delivery Time</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cost</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(option, index) in shippingOptions" :key="index">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ option.method }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ option.time }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ option.cost }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Shipping Policies</h2>
          
          <div class="space-y-4">
            <div class="border-l-4 border-rose-gold pl-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">Order Processing</h3>
              <p class="text-gray-600">All orders are processed within 1-2 business days after payment confirmation. Orders placed on weekends or holidays will be processed on the next business day.</p>
            </div>
            
            <div class="border-l-4 border-rose-gold pl-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">Shipping Destinations</h3>
              <p class="text-gray-600">We ship to all 50 US states and over 100 countries worldwide. Some restrictions may apply for certain international destinations due to customs regulations.</p>
            </div>
            
            <div class="border-l-4 border-rose-gold pl-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">Tracking Information</h3>
              <p class="text-gray-600">Once your order ships, you will receive a shipping confirmation email with tracking information. You can also track your order by logging into your account and viewing your order history.</p>
            </div>
            
            <div class="border-l-4 border-rose-gold pl-4">
              <h3 class="text-lg font-medium text-gray-900 mb-2">International Shipping</h3>
              <p class="text-gray-600">International customers are responsible for all duties, import taxes, and customs fees that may be incurred. These charges are not included in the purchase price or shipping cost.</p>
            </div>
          </div>
        </section>
        
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Frequently Asked Questions</h2>
          
          <div class="space-y-4">
            <div v-for="(faq, index) in faqs" :key="index" class="border border-gray-200 rounded-lg p-4">
              <button 
                @click="faq.isOpen = !faq.isOpen"
                class="flex justify-between items-center w-full text-left font-medium text-gray-900 focus:outline-none"
              >
                <span>{{ faq.question }}</span>
                <Icon :name="faq.isOpen ? 'ph:caret-up' : 'ph:caret-down'" class="h-5 w-5 text-gray-500" />
              </button>
              <div v-show="faq.isOpen" class="mt-4 text-gray-600">
                <p>{{ faq.answer }}</p>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const shippingOptions = ref([
  {
    method: 'Standard Shipping',
    time: '3-5 business days',
    cost: 'Free on orders over $75, otherwise $5.95'
  },
  {
    method: 'Express Shipping',
    time: '2 business days',
    cost: '$12.95'
  },
  {
    method: 'Next Day Shipping',
    time: '1 business day',
    cost: '$24.95'
  },
  {
    method: 'International Standard',
    time: '7-14 business days',
    cost: 'Starting at $15.95'
  },
  {
    method: 'International Express',
    time: '3-5 business days',
    cost: 'Starting at $29.95'
  }
]);

const faqs = ref([
  {
    question: 'When will my order ship?',
    answer: 'Orders are typically processed within 1-2 business days after payment confirmation. You will receive a shipping confirmation email with tracking information once your order ships.',
    isOpen: false
  },
  {
    question: 'Do you ship to PO boxes?',
    answer: 'Yes, we ship to PO boxes for standard shipping only. Express and Next Day shipping options require a physical address.',
    isOpen: false
  },
  {
    question: 'Can I change my shipping address after placing an order?',
    answer: 'Address changes can only be accommodated if the order has not yet been processed. Please contact customer service immediately if you need to change your shipping address.',
    isOpen: false
  },
  {
    question: 'What happens if my package is lost or damaged?',
    answer: 'If your package is lost or damaged during transit, please contact our customer service team within 7 days of the expected delivery date. We will work with the shipping carrier to resolve the issue.',
    isOpen: false
  }
]);
</script>