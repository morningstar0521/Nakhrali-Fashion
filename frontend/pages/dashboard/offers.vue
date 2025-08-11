<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-5xl mx-auto">
      <!-- Page Header -->
      <div class="mb-8 text-center md:text-left">
        <h1 class="text-3xl font-display font-bold text-deep-maroon mb-2">
          Special Offers
        </h1>
        <p class="text-gray-600">
          Exclusive deals and promotions just for you
        </p>
      </div>
      
      <!-- Loading State -->
      <div v-if="isLoading" class="flex justify-center items-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-rose-gold"></div>
      </div>
      
      <!-- Offers Grid -->
      <div v-else-if="offers.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div 
          v-for="offer in offers" 
          :key="offer.id" 
          class="bg-white rounded-lg shadow-md overflow-hidden border border-gray-100 hover:shadow-lg transition-shadow duration-300"
        >
          <!-- Offer Image -->
          <div class="relative">
            <img :src="offer.image" :alt="offer.title" class="w-full h-48 object-cover" />
            <div 
              v-if="offer.expiresIn <= 3" 
              class="absolute top-3 right-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full"
            >
              Expires {{ offer.expiresIn === 0 ? 'Today' : `in ${offer.expiresIn} days` }}!
            </div>
          </div>
          
          <!-- Offer Content -->
          <div class="p-5">
            <div class="flex justify-between items-start mb-2">
              <h2 class="text-xl font-display font-bold text-gray-900 leading-tight">{{ offer.title }}</h2>
              <span class="bg-rose-gold/10 text-deep-maroon text-lg font-bold px-2 py-1 rounded">
                {{ offer.discount }}
              </span>
            </div>
            
            <p class="text-gray-600 mb-4">{{ offer.description }}</p>
            
            <div class="flex items-center justify-between text-sm text-gray-500 mb-4">
              <span class="flex items-center">
                <Icon name="ph:calendar" class="mr-1 h-4 w-4" />
                Valid till: {{ formatDate(offer.validUntil) }}
              </span>
              <span v-if="offer.usageLimit" class="flex items-center">
                <Icon name="ph:repeat" class="mr-1 h-4 w-4" />
                {{ offer.usageLimit }} uses
              </span>
            </div>
            
            <!-- Offer Code -->
            <div v-if="offer.code" class="mb-4">
              <div class="relative">
                <input 
                  type="text" 
                  :value="offer.code" 
                  readonly 
                  class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-md text-gray-700 font-mono text-center focus:outline-none"
                />
                <button 
                  @click="copyCode(offer.code)" 
                  class="absolute right-2 top-1/2 transform -translate-y-1/2 text-rose-gold hover:text-deep-maroon"
                  :title="`Copy code: ${offer.code}`"
                >
                  <Icon name="ph:copy" class="h-5 w-5" />
                </button>
              </div>
            </div>
            
            <!-- Action Button -->
            <NuxtLink 
              :to="offer.link" 
              class="block w-full text-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold transition-colors duration-200"
            >
              {{ offer.buttonText || 'Shop Now' }}
            </NuxtLink>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else class="bg-white rounded-lg shadow-md p-8 text-center">
        <div class="mx-auto w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
          <Icon name="ph:gift" class="h-8 w-8 text-gray-400" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 mb-1">No offers available</h3>
        <p class="text-gray-500 mb-4">We don't have any special offers for you at the moment. Check back soon!</p>
        <NuxtLink to="/products" class="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
          Browse Products
        </NuxtLink>
      </div>
      
      <!-- Recommended Products -->
      <div v-if="recommendedProducts.length > 0" class="mt-12">
        <h2 class="text-2xl font-display font-bold text-deep-maroon mb-6">
          Recommended For You
        </h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div 
            v-for="product in recommendedProducts" 
            :key="product.id" 
            class="bg-white rounded-lg shadow-sm overflow-hidden border border-gray-100 hover:shadow-md transition-shadow duration-300"
          >
            <NuxtLink :to="`/products/${product.id}`">
              <img :src="product.image" :alt="product.name" class="w-full h-48 object-cover" />
              <div class="p-4">
                <h3 class="text-gray-900 font-medium mb-1 truncate">{{ product.name }}</h3>
                <div class="flex justify-between items-center">
                  <span class="text-deep-maroon font-bold">₹{{ formatPrice(product.price) }}</span>
                  <span v-if="product.originalPrice" class="text-gray-500 text-sm line-through">₹{{ formatPrice(product.originalPrice) }}</span>
                </div>
              </div>
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
import { ref, onMounted } from 'vue';
import { format, parseISO, differenceInDays } from 'date-fns';

// SEO
useHead({
  title: 'Special Offers - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Exclusive deals and promotions for Nakhrali Fashion customers.'
    }
  ]
});

// Auth
const { user } = useAuth();
const config = useRuntimeConfig();
const apiBase = config.public.apiBase;
const toast = useToast();

// Data
const offers = ref([]);
const recommendedProducts = ref([]);
const isLoading = ref(true);

// Mock data for offers
const mockOffers = [
  {
    id: 1,
    title: 'First Purchase Discount',
    description: 'Get 15% off on your first purchase with us. Apply this code at checkout.',
    discount: '15% OFF',
    code: 'FIRST15',
    validUntil: new Date(new Date().setDate(new Date().getDate() + 30)).toISOString(),
    expiresIn: 30,
    image: 'https://via.placeholder.com/600/FFD700/000000?text=15%+OFF',
    link: '/products',
    buttonText: 'Shop Now',
    usageLimit: 1
  },
  {
    id: 2,
    title: 'Birthday Special',
    description: 'Happy Birthday! Enjoy a special discount on all jewelry items this month.',
    discount: '₹1000 OFF',
    code: 'BDAY1000',
    validUntil: new Date(new Date().setDate(new Date().getDate() + 7)).toISOString(),
    expiresIn: 7,
    image: 'https://via.placeholder.com/600/FFC0CB/000000?text=Birthday+Special',
    link: '/products/category/jewelry',
    buttonText: 'Claim Now'
  },
  {
    id: 3,
    title: 'Weekend Flash Sale',
    description: 'Limited time offer! Get amazing discounts on selected items this weekend only.',
    discount: 'Up to 30% OFF',
    validUntil: new Date(new Date().setDate(new Date().getDate() + 2)).toISOString(),
    expiresIn: 2,
    image: 'https://via.placeholder.com/600/FF4500/FFFFFF?text=Flash+Sale',
    link: '/products/sale',
    buttonText: 'Shop Sale'
  },
  {
    id: 4,
    title: 'Free Shipping',
    description: 'Enjoy free shipping on all orders above ₹2999. No coupon needed, automatically applied at checkout.',
    discount: 'FREE SHIPPING',
    validUntil: new Date(new Date().setDate(new Date().getDate() + 0)).toISOString(),
    expiresIn: 0,
    image: 'https://via.placeholder.com/600/4169E1/FFFFFF?text=Free+Shipping',
    link: '/products',
    buttonText: 'Shop Now'
  },
  {
    id: 5,
    title: 'Loyalty Reward',
    description: 'Thank you for being a loyal customer! Here\'s a special discount just for you.',
    discount: '10% OFF',
    code: 'LOYAL10',
    validUntil: new Date(new Date().setDate(new Date().getDate() + 14)).toISOString(),
    expiresIn: 14,
    image: 'https://via.placeholder.com/600/9932CC/FFFFFF?text=Loyalty+Reward',
    link: '/products',
    buttonText: 'Redeem Now',
    usageLimit: 3
  }
];

// Mock data for recommended products
const mockRecommendedProducts = [
  {
    id: 1,
    name: 'Gold Plated Kundan Necklace Set',
    price: 8499,
    originalPrice: 9999,
    image: 'https://via.placeholder.com/300/FFD700/000000?text=Necklace'
  },
  {
    id: 2,
    name: 'Pearl Embellished Jhumkas',
    price: 2250,
    image: 'https://via.placeholder.com/300/C0C0C0/000000?text=Jhumkas'
  },
  {
    id: 3,
    name: 'Ruby Studded Bangles Set',
    price: 5999,
    originalPrice: 7499,
    image: 'https://via.placeholder.com/300/E0115F/FFFFFF?text=Bangles'
  },
  {
    id: 4,
    name: 'Traditional Maang Tikka',
    price: 3499,
    image: 'https://via.placeholder.com/300/B8860B/FFFFFF?text=Maang+Tikka'
  }
];

// Load offers and recommended products
onMounted(async () => {
  isLoading.value = true;
  
  try {
    // In a real app, fetch from API
    // const [offersResponse, productsResponse] = await Promise.all([
    //   $fetch(`${apiBase}/offers`, {
    //     method: 'GET',
    //     headers: {
    //       'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    //     }
    //   }),
    //   $fetch(`${apiBase}/products/recommended`, {
    //     method: 'GET',
    //     headers: {
    //       'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    //     }
    //   })
    // ]);
    // 
    // offers.value = offersResponse.offers;
    // recommendedProducts.value = productsResponse.products;
    
    // Using mock data for demo
    setTimeout(() => {
      offers.value = mockOffers;
      recommendedProducts.value = mockRecommendedProducts;
      isLoading.value = false;
    }, 800);
  } catch (error) {
    console.error('Failed to load offers:', error);
    isLoading.value = false;
    toast.error('Failed to load offers. Please try again later.');
  }
});

// Format date
const formatDate = (dateString) => {
  try {
    return format(parseISO(dateString), 'MMM d, yyyy');
  } catch (error) {
    return dateString;
  }
};

// Format price
const formatPrice = (price) => {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
};

// Copy code to clipboard
const copyCode = (code) => {
  navigator.clipboard.writeText(code)
    .then(() => {
      toast.success(`Code ${code} copied to clipboard!`);
    })
    .catch(() => {
      toast.error('Failed to copy code. Please try manually.');
    });
};

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
});
</script>