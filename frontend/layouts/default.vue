<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-white dark:bg-gray-900 shadow-soft dark:shadow-none sticky top-0 z-40">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-16 lg:h-20">
          <!-- Logo -->
          <NuxtLink to="/" class="flex items-center space-x-2">
            <div class="w-10 h-10 bg-gradient-luxury rounded-full flex items-center justify-center">
              <span class="text-white font-luxury text-lg">N</span>
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-display text-gray-900 dark:text-white">Nakhrali Fashion</h1>
              <p class="text-xs text-gray-500 dark:text-gray-400">Where Elegance Meets Emotion</p>
            </div>
          </NuxtLink>

          <!-- Desktop Navigation -->
          <nav class="hidden lg:flex items-center space-x-8">
            <NuxtLink 
              v-for="item in navigationItems" 
              :key="item.path"
              :to="item.path"
              class="nav-link"
              :class="{ 'active': $route.path === item.path }"
            >
              {{ item.name }}
            </NuxtLink>
          </nav>

          <!-- Right Side Actions -->
          <div class="flex items-center space-x-4">
            <!-- Theme Toggle -->
            <ThemeToggle class="hidden md:flex" />
            
            <!-- Search -->
            <button 
              @click="toggleSearch"
              class="p-2 text-gray-600 hover:text-rose-gold transition-colors"
            >
              <Icon name="heroicons:magnifying-glass" class="w-5 h-5" />
            </button>

            <!-- User Menu -->
            <div v-if="isAuthenticated" class="relative">
              <button 
                @click="toggleUserMenu"
                class="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div class="w-8 h-8 bg-rose-gold rounded-full flex items-center justify-center">
                  <span class="text-white text-sm font-medium">
                    {{ userFullName.charAt(0) || user?.email?.charAt(0) }}
                  </span>
                </div>
                <Icon name="heroicons:chevron-down" class="w-4 h-4" />
              </button>

              <!-- User Dropdown -->
              <div 
                v-if="showUserMenu"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-large border border-gray-200 py-2 z-50"
              >
                <NuxtLink 
                  to="/account"
                  class="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                >
                  My Account
                </NuxtLink>
                <NuxtLink 
                  to="/orders"
                  class="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                >
                  My Orders
                </NuxtLink>
                <NuxtLink 
                  to="/wishlist"
                  class="block px-4 py-2 text-gray-700 hover:bg-gray-100"
                >
                  Wishlist
                </NuxtLink>
                <hr class="my-2">
                <button 
                  @click="logout"
                  class="block w-full text-left px-4 py-2 text-gray-700 hover:bg-gray-100"
                >
                  Logout
                </button>
              </div>
            </div>

            <!-- Login/Register -->
            <div v-else class="flex items-center space-x-2">
              <NuxtLink 
                to="/auth/login"
                class="btn-outline text-sm"
              >
                Login
              </NuxtLink>
              <NuxtLink 
                to="/auth/register"
                class="btn-primary text-sm"
              >
                Register
              </NuxtLink>
            </div>

            <!-- Cart -->
            <NuxtLink 
              to="/cart"
              class="relative p-2 text-gray-600 hover:text-rose-gold transition-colors"
            >
              <Icon name="heroicons:shopping-bag" class="w-5 h-5" />
              <span 
                v-if="cartItemCount > 0"
                class="absolute -top-1 -right-1 bg-rose-gold text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
              >
                {{ cartItemCount }}
              </span>
            </NuxtLink>

            <!-- Mobile Menu Button -->
            <button 
              @click="toggleMobileMenu"
              class="lg:hidden p-2 text-gray-600 hover:text-rose-gold transition-colors"
            >
              <Icon name="heroicons:bars-3" class="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>

      <!-- Search Bar -->
      <div 
        v-if="showSearch"
        class="border-t border-gray-200 bg-white py-4"
      >
        <div class="container mx-auto px-4">
          <div class="relative">
            <input 
              v-model="searchQuery"
              @keyup.enter="performSearch"
              type="text"
              placeholder="Search for jewelry..."
              class="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent"
            >
            <Icon 
              name="heroicons:magnifying-glass" 
              class="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400"
            />
          </div>
        </div>
      </div>
    </header>

    <!-- Mobile Menu -->
    <div 
      v-if="showMobileMenu"
      class="lg:hidden fixed inset-0 bg-black bg-opacity-50 z-50"
      @click="closeMobileMenu"
    >
      <div 
        class="absolute right-0 top-0 h-full w-64 bg-white shadow-large"
        @click.stop
      >
        <div class="p-4">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-lg font-display">Menu</h2>
            <div class="flex items-center space-x-2">
              <ThemeToggle />
              <button 
                @click="closeMobileMenu"
                class="p-2 text-gray-600 hover:text-rose-gold"
              >
                <Icon name="heroicons:x-mark" class="w-5 h-5" />
              </button>
            </div>
          </div>

          <nav class="space-y-4">
            <NuxtLink 
              v-for="item in navigationItems" 
              :key="item.path"
              :to="item.path"
              class="block py-2 text-gray-700 hover:text-rose-gold transition-colors"
              @click="closeMobileMenu"
            >
              {{ item.name }}
            </NuxtLink>
          </nav>

          <hr class="my-6">

          <div v-if="user" class="space-y-4">
            <NuxtLink 
              to="/account"
              class="block py-2 text-gray-700 hover:text-rose-gold"
              @click="closeMobileMenu"
            >
              My Account
            </NuxtLink>
            <NuxtLink 
              to="/orders"
              class="block py-2 text-gray-700 hover:text-rose-gold"
              @click="closeMobileMenu"
            >
              My Orders
            </NuxtLink>
            <button 
              @click="logout"
              class="block w-full text-left py-2 text-gray-700 hover:text-rose-gold"
            >
              Logout
            </button>
          </div>
          <div v-else class="space-y-2">
            <NuxtLink 
              to="/auth/login"
              class="block w-full text-center py-2 border border-rose-gold text-rose-gold rounded-lg"
              @click="closeMobileMenu"
            >
              Login
            </NuxtLink>
            <NuxtLink 
              to="/auth/register"
              class="block w-full text-center py-2 bg-rose-gold text-white rounded-lg"
              @click="closeMobileMenu"
            >
              Register
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white dark:bg-gray-950">
      <div class="container mx-auto px-4 py-12">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <!-- Company Info -->
          <div>
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-8 h-8 bg-gradient-luxury rounded-full flex items-center justify-center">
                <span class="text-white font-luxury">N</span>
              </div>
              <h3 class="text-lg font-display">Nakhrali Fashion</h3>
            </div>
            <p class="text-gray-400 mb-4">
              Where Elegance Meets Emotion. Discover our exquisite collection of ethnic jewelry.
            </p>
            <div class="flex space-x-4">
              <a href="#" class="text-gray-400 hover:text-rose-gold transition-colors">
                <Icon name="heroicons:envelope" class="w-5 h-5" />
              </a>
              <a href="#" class="text-gray-400 hover:text-rose-gold transition-colors">
                <Icon name="heroicons:phone" class="w-5 h-5" />
              </a>
              <a href="#" class="text-gray-400 hover:text-rose-gold transition-colors">
                <Icon name="heroicons:map-pin" class="w-5 h-5" />
              </a>
            </div>
          </div>

          <!-- Quick Links -->
          <div>
            <h4 class="text-lg font-display mb-4">Quick Links</h4>
            <ul class="space-y-2">
              <li>
                <NuxtLink to="/products" class="footer-link">All Products</NuxtLink>
              </li>
              <li>
                <NuxtLink to="/collections" class="footer-link">Collections</NuxtLink>
              </li>
              <li>
                <NuxtLink to="/about" class="footer-link">About Us</NuxtLink>
              </li>
              <li>
                <NuxtLink to="/contact" class="footer-link">Contact</NuxtLink>
              </li>
            </ul>
          </div>

          <!-- Customer Service -->
          <div>
            <h4 class="text-lg font-display mb-4">Customer Service</h4>
            <ul class="space-y-2">
              <li>
                <NuxtLink to="/help" class="footer-link">Help Center</NuxtLink>
              </li>
              <li>
                <NuxtLink to="/shipping" class="footer-link">Shipping Info</NuxtLink>
              </li>
              <li>
                <NuxtLink to="/returns" class="footer-link">Returns & Exchanges</NuxtLink>
              </li>
              <li>
                <NuxtLink to="/size-guide" class="footer-link">Size Guide</NuxtLink>
              </li>
            </ul>
          </div>

          <!-- Newsletter -->
          <div>
            <h4 class="text-lg font-display mb-4">Stay Updated</h4>
            <p class="text-gray-400 mb-4">
              Subscribe to our newsletter for exclusive offers and updates.
            </p>
            <form @submit.prevent="subscribeNewsletter" class="space-y-2">
              <input 
                v-model="newsletterEmail"
                type="email"
                placeholder="Enter your email"
                class="w-full px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-rose-gold focus:border-transparent"
              >
              <button 
                type="submit"
                class="w-full btn-primary text-sm"
              >
                Subscribe
              </button>
            </form>
          </div>
        </div>

        <hr class="my-8 border-gray-800">

        <!-- Bottom Footer -->
        <div class="flex flex-col md:flex-row justify-between items-center">
          <p class="text-gray-400 text-sm">
            © 2024 Nakhrali Fashion. All rights reserved.
          </p>
          <div class="flex space-x-6 mt-4 md:mt-0">
            <NuxtLink to="/privacy" class="footer-link text-sm">Privacy Policy</NuxtLink>
            <NuxtLink to="/terms" class="footer-link text-sm">Terms of Service</NuxtLink>
            <NuxtLink to="/sitemap" class="footer-link text-sm">Sitemap</NuxtLink>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useToast } from 'vue-toastification'
import ThemeToggle from '~/components/ThemeToggle.vue'

// Navigation items
const navigationItems = [
  { name: 'Home', path: '/' },
  { name: 'Products', path: '/products' },
  { name: 'Collections', path: '/collections' },
  { name: 'About', path: '/about' },
  { name: 'Contact', path: '/contact' }
]

// Reactive state
const showSearch = ref(false)
const showUserMenu = ref(false)
const showMobileMenu = ref(false)
const searchQuery = ref('')
const newsletterEmail = ref('')

// Auth state
const { user, isAuthenticated, logout: authLogout, userFullName } = useAuth()
const toast = useToast()

// Cart state (from stores)
const cartItemCount = ref(0) // Will be connected to cart store

// Methods
const toggleSearch = () => {
  showSearch.value = !showSearch.value
  if (!showSearch.value) {
    searchQuery.value = ''
  }
}

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
}

const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const performSearch = () => {
  if (searchQuery.value.trim()) {
    navigateTo(`/search?q=${encodeURIComponent(searchQuery.value)}`)
    showSearch.value = false
    searchQuery.value = ''
  }
}

const logout = async () => {
  await authLogout()
  showUserMenu.value = false
  toast.success('Logged out successfully!')
}

const subscribeNewsletter = async () => {
  if (newsletterEmail.value) {
    // Will be implemented with API call
    console.log('Subscribe to newsletter:', newsletterEmail.value)
    newsletterEmail.value = ''
  }
}

// Close dropdowns when clicking outside
onMounted(() => {
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.user-menu')) {
      showUserMenu.value = false
    }
  })
})

// Watch for route changes to close mobile menu
watch(() => useRoute().path, () => {
  closeMobileMenu()
})
</script>