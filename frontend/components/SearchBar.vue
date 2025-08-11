<template>
  <div class="search-container relative">
    <!-- Search Input -->
    <div class="relative">
      <input
        v-model="searchQuery"
        @focus="showDropdown = true"
        @keyup.enter="handleSearch"
        type="text"
        placeholder="Search for products..."
        class="w-full pl-10 pr-4 py-2 border rounded-full focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
      />
      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
      </div>
      <button 
        v-if="searchQuery" 
        @click="clearSearch"
        class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <!-- Search Dropdown -->
    <div 
      v-if="showDropdown && (quickResults.length > 0 || recentSearches.length > 0)" 
      class="absolute z-10 mt-1 w-full bg-white rounded-md shadow-lg max-h-96 overflow-y-auto"
      v-click-outside="closeDropdown"
    >
      <!-- Quick Results -->
      <div v-if="quickResults.length > 0" class="py-2">
        <h3 class="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">Products</h3>
        <ul>
          <li 
            v-for="result in quickResults" 
            :key="result.id"
            @click="navigateToProduct(result.id)"
            class="px-4 py-2 hover:bg-gray-100 cursor-pointer"
          >
            <div class="flex items-center">
              <img 
                :src="result.main_image || '/images/placeholder.png'" 
                :alt="result.name"
                class="w-10 h-10 object-cover rounded-md mr-3"
              />
              <div>
                <div class="font-medium">{{ result.name }}</div>
                <div class="text-sm text-gray-500">{{ formatPrice(result.price) }}</div>
              </div>
            </div>
          </li>
        </ul>
        <div class="px-4 py-2 border-t">
          <button 
            @click="handleSearch"
            class="text-primary hover:text-primary-dark text-sm font-medium"
          >
            See all results for "{{ searchQuery }}"
          </button>
        </div>
      </div>

      <!-- Recent Searches -->
      <div v-if="recentSearches.length > 0 && !isSearching" class="py-2 border-t">
        <div class="px-4 py-2 flex justify-between items-center">
          <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">Recent Searches</h3>
          <button 
            @click="clearRecentSearches"
            class="text-xs text-gray-500 hover:text-gray-700"
          >
            Clear
          </button>
        </div>
        <ul>
          <li 
            v-for="(search, index) in recentSearches" 
            :key="index"
            @click="searchWithTerm(search)"
            class="px-4 py-2 hover:bg-gray-100 cursor-pointer flex items-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-gray-400 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            {{ search }}
          </li>
        </ul>
      </div>

      <!-- Loading State -->
      <div v-if="isSearching" class="py-8 flex justify-center">
        <div class="animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-primary"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSearch } from '~/composables/useSearch'
import debounce from 'lodash/debounce'

const props = defineProps({
  placeholder: {
    type: String,
    default: 'Search for products...'
  },
  autoFocus: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()
const { 
  searchQuery: globalSearchQuery,
  recentSearches,
  isSearching,
  quickSearch,
  navigateToSearch,
  clearSearch: clearGlobalSearch,
  clearRecentSearches
} = useSearch()

const searchQuery = ref('')
const quickResults = ref([])
const showDropdown = ref(false)
const searchInput = ref(null)

// Sync with global search query
watch(globalSearchQuery, (newVal) => {
  searchQuery.value = newVal
})

watch(searchQuery, debounce(async (newVal) => {
  if (newVal && newVal.length >= 2) {
    globalSearchQuery.value = newVal
    quickResults.value = await quickSearch(newVal)
  } else {
    quickResults.value = []
  }
}, 300))

onMounted(() => {
  if (props.autoFocus && searchInput.value) {
    searchInput.value.focus()
  }
})

const handleSearch = () => {
  if (!searchQuery.value) return
  navigateToSearch(searchQuery.value)
  showDropdown.value = false
}

const searchWithTerm = (term) => {
  searchQuery.value = term
  globalSearchQuery.value = term
  navigateToSearch(term)
  showDropdown.value = false
}

const navigateToProduct = (productId) => {
  router.push(`/products/${productId}`)
  showDropdown.value = false
}

const clearSearch = () => {
  searchQuery.value = ''
  globalSearchQuery.value = ''
  clearGlobalSearch()
  quickResults.value = []
}

const closeDropdown = () => {
  showDropdown.value = false
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR'
  }).format(price)
}

// Custom directive for clicking outside
const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (event) => {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutside)
  }
}
</script>