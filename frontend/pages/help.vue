<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 class="text-3xl font-display font-bold text-deep-maroon mb-8">Help Center</h1>
      
      <div class="space-y-8">
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
        
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Contact Us</h2>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Customer Support</h3>
              <p class="text-gray-600 mb-4">Our team is available to assist you with any questions or concerns.</p>
              
              <div class="space-y-3">
                <div class="flex items-center">
                  <Icon name="ph:envelope" class="h-5 w-5 text-rose-gold mr-2" />
                  <span>support@nakhrali.com</span>
                </div>
                <div class="flex items-center">
                  <Icon name="ph:phone" class="h-5 w-5 text-rose-gold mr-2" />
                  <span>+1 (800) 123-4567</span>
                </div>
                <div class="flex items-center">
                  <Icon name="ph:clock" class="h-5 w-5 text-rose-gold mr-2" />
                  <span>Monday - Friday, 9am - 6pm EST</span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 class="text-lg font-medium text-gray-900 mb-2">Send Us a Message</h3>
              <form class="space-y-4">
                <div>
                  <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Name</label>
                  <input type="text" id="name" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold" />
                </div>
                <div>
                  <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input type="email" id="email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold" />
                </div>
                <div>
                  <label for="message" class="block text-sm font-medium text-gray-700 mb-1">Message</label>
                  <textarea id="message" rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold focus:border-rose-gold"></textarea>
                </div>
                <button type="submit" class="w-full bg-rose-gold hover:bg-deep-maroon text-white font-medium py-2 px-4 rounded-md transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
                  Send Message
                </button>
              </form>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const faqs = ref([
  {
    question: 'How do I track my order?',
    answer: 'You can track your order by logging into your account and visiting the Order History section. Alternatively, you can use the tracking number provided in your shipping confirmation email.',
    isOpen: false
  },
  {
    question: 'What payment methods do you accept?',
    answer: 'We accept all major credit cards (Visa, MasterCard, American Express, Discover), PayPal, and Apple Pay.',
    isOpen: false
  },
  {
    question: 'How long does shipping take?',
    answer: 'Standard shipping typically takes 3-5 business days within the continental US. Express shipping options are available at checkout for 1-2 business day delivery.',
    isOpen: false
  },
  {
    question: 'Do you ship internationally?',
    answer: 'Yes, we ship to most countries worldwide. International shipping times vary by location, typically ranging from 7-14 business days.',
    isOpen: false
  },
  {
    question: 'What is your return policy?',
    answer: 'We offer a 30-day return policy for unworn items in their original packaging. Please visit our Returns & Exchanges page for more details.',
    isOpen: false
  }
]);
</script>