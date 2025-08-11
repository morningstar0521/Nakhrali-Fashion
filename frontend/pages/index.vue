<template>
  <div>
    <!-- Hero Section -->
    <section class="relative h-screen flex items-center justify-center overflow-hidden">
      <!-- Background Video/Image -->
      <div class="absolute inset-0 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20">
        <div class="absolute inset-0 bg-black/30"></div>
      </div>
      
      <!-- Hero Content -->
      <div class="relative z-10 text-center text-white px-4">
        <h1 class="text-5xl md:text-7xl font-display mb-6 animate-fade-in">
          Where Elegance
          <span class="block gradient-text">Meets Emotion</span>
        </h1>
        <p class="text-xl md:text-2xl font-body mb-8 max-w-2xl mx-auto animate-fade-in">
          Discover our exquisite collection of ethnic jewelry, crafted with love and tradition
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center animate-fade-in">
          <NuxtLink 
            to="/products"
            class="btn-primary text-lg px-8 py-4"
          >
            Shop Now
          </NuxtLink>
          <NuxtLink 
            to="/collections"
            class="btn-secondary text-lg px-8 py-4"
          >
            View Collections
          </NuxtLink>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <Icon name="heroicons:chevron-down" class="w-6 h-6 text-white" />
      </div>
    </section>

    <!-- Categories Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-display text-gray-900 mb-4">Shop by Category</h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Explore our diverse collection of jewelry for every occasion
          </p>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div 
            v-for="category in categories" 
            :key="category.id"
            class="group cursor-pointer"
            @click="navigateToCategory(category.slug)"
          >
            <div class="relative overflow-hidden rounded-xl bg-gray-100 aspect-square mb-4">
              <img 
                :src="category.image || '/images/placeholder.jpg'" 
                :alt="category.name"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              >
              <div class="absolute inset-0 bg-black/20 group-hover:bg-black/40 transition-colors duration-300"></div>
            </div>
            <h3 class="text-lg font-display text-gray-900 text-center">{{ category.name }}</h3>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="py-16 bg-ivory">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-display text-gray-900 mb-4">Featured Products</h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Handpicked pieces that embody luxury and tradition
          </p>
        </div>

        <div v-if="featuredProducts.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <ProductCard 
            v-for="product in featuredProducts" 
            :key="product.id"
            :product="product"
          />
        </div>

        <div v-else class="text-center py-12">
          <div class="spinner w-8 h-8 mx-auto mb-4"></div>
          <p class="text-gray-600">Loading featured products...</p>
        </div>

        <div class="text-center mt-12">
          <NuxtLink 
            to="/products"
            class="btn-primary text-lg px-8 py-4"
          >
            View All Products
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- Collections Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-display text-gray-900 mb-4">Special Collections</h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            Curated collections for every special moment
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div 
            v-for="collection in collections" 
            :key="collection.id"
            class="group cursor-pointer"
            @click="navigateToCollection(collection.slug)"
          >
            <div class="relative overflow-hidden rounded-xl aspect-[4/5] mb-4">
              <img 
                :src="collection.banner_image || collection.image || '/images/placeholder.jpg'" 
                :alt="collection.name"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              >
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
              <div class="absolute bottom-0 left-0 right-0 p-6 text-white">
                <h3 class="text-2xl font-display mb-2">{{ collection.name }}</h3>
                <p class="text-sm opacity-90">{{ collection.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section class="py-16 bg-gray-50">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-display text-gray-900 mb-4">Why Choose Nakhrali Fashion</h2>
          <p class="text-lg text-gray-600 max-w-2xl mx-auto">
            We bring you the finest jewelry with unmatched quality and service
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-luxury rounded-full flex items-center justify-center mx-auto mb-4">
              <Icon name="heroicons:sparkles" class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-display text-gray-900 mb-2">Premium Quality</h3>
            <p class="text-gray-600">
              Each piece is crafted with the finest materials and attention to detail
            </p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-luxury rounded-full flex items-center justify-center mx-auto mb-4">
              <Icon name="heroicons:truck" class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-display text-gray-900 mb-2">Free Shipping</h3>
            <p class="text-gray-600">
              Complimentary shipping on orders above ₹5000 across India
            </p>
          </div>

          <div class="text-center">
            <div class="w-16 h-16 bg-gradient-luxury rounded-full flex items-center justify-center mx-auto mb-4">
              <Icon name="heroicons:shield-check" class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-xl font-display text-gray-900 mb-2">Secure Shopping</h3>
            <p class="text-gray-600">
              Your security is our priority with encrypted payments and data protection
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Newsletter Section -->
    <section class="py-16 bg-gradient-luxury">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-display text-white mb-4">Stay Updated</h2>
        <p class="text-xl text-white/90 mb-8 max-w-2xl mx-auto">
          Subscribe to our newsletter for exclusive offers, new collections, and jewelry care tips
        </p>
        
        <form @submit.prevent="subscribeNewsletter" class="max-w-md mx-auto">
          <div class="flex gap-4">
            <input 
              v-model="newsletterEmail"
              type="email"
              placeholder="Enter your email"
              class="flex-1 px-4 py-3 rounded-lg border-0 focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-rose-gold"
              required
            >
            <button 
              type="submit"
              class="px-6 py-3 bg-white text-rose-gold font-medium rounded-lg hover:bg-gray-100 transition-colors"
            >
              Subscribe
            </button>
          </div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Nakhrali Fashion - Where Elegance Meets Emotion',
  meta: [
    {
      name: 'description',
      content: 'Discover exquisite ethnic jewelry at Nakhrali Fashion. Premium gold, silver, and diamond jewelry for every occasion. Bridal, casual, and party wear collections.'
    }
  ]
})

// Reactive data
const featuredProducts = ref([])
const categories = ref([])
const collections = ref([])
const newsletterEmail = ref('')

// Sample data (will be replaced with API calls)
const sampleCategories = [
  { id: 1, name: 'Rings', slug: 'rings', image: '/images/categories/rings.jpg' },
  { id: 2, name: 'Earrings', slug: 'earrings', image: '/images/categories/earrings.jpg' },
  { id: 3, name: 'Necklaces', slug: 'necklaces', image: '/images/categories/necklaces.jpg' },
  { id: 4, name: 'Bangles', slug: 'bangles', image: '/images/categories/bangles.jpg' }
]

const sampleCollections = [
  {
    id: 1,
    name: 'Bridal Collection',
    slug: 'bridal',
    description: 'Perfect jewelry for your special day',
    banner_image: '/images/collections/bridal.jpg'
  },
  {
    id: 2,
    name: 'Festive Collection',
    slug: 'festive',
    description: 'Celebrate festivals with our stunning pieces',
    banner_image: '/images/collections/festive.jpg'
  },
  {
    id: 3,
    name: 'Office Wear',
    slug: 'office-wear',
    description: 'Elegant jewelry for the modern professional',
    banner_image: '/images/collections/office.jpg'
  }
]

// Methods
const navigateToCategory = (slug) => {
  navigateTo(`/products?category=${slug}`)
}

const navigateToCollection = (slug) => {
  navigateTo(`/collections/${slug}`)
}

const subscribeNewsletter = async () => {
  if (newsletterEmail.value) {
    try {
      // API call to subscribe
      console.log('Subscribing to newsletter:', newsletterEmail.value)
      newsletterEmail.value = ''
      // Show success message
    } catch (error) {
      console.error('Newsletter subscription failed:', error)
    }
  }
}

// Load data
onMounted(async () => {
  try {
    // Load featured products
    // const response = await $fetch('/api/products/featured')
    // featuredProducts.value = response.featured_products
    
    // Load categories
    // const categoriesResponse = await $fetch('/api/products/categories')
    // categories.value = categoriesResponse.categories
    
    // Load collections
    // const collectionsResponse = await $fetch('/api/products/collections')
    // collections.value = collectionsResponse.collections
    
    // For now, use sample data
    categories.value = sampleCategories
    collections.value = sampleCollections
  } catch (error) {
    console.error('Failed to load home page data:', error)
  }
})
</script> 