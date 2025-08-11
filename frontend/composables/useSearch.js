import { ref, computed, watch } from 'vue'
import { useRuntimeConfig } from '#app'
import { useToast } from 'vue-toastification'
import { useRouter } from 'vue-router'

export function useSearch() {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBaseURL || '/api'
  const toast = useToast()
  const router = useRouter()

  // State
  const searchQuery = ref('')
  const searchResults = ref([])
  const isSearching = ref(false)
  const searchError = ref(null)
  const recentSearches = ref([])
  const showSearchModal = ref(false)
  const searchFilters = ref({
    category: null,
    price_min: null,
    price_max: null,
    material: null,
    occasion: null,
    style: null,
    sort_by: 'relevance'
  })

  // Load recent searches from localStorage
  const loadRecentSearches = () => {
    try {
      const saved = localStorage.getItem('recentSearches')
      if (saved) {
        recentSearches.value = JSON.parse(saved)
      }
    } catch (err) {
      console.error('Error loading recent searches:', err)
    }
  }

  // Save recent searches to localStorage
  const saveRecentSearches = () => {
    try {
      localStorage.setItem('recentSearches', JSON.stringify(recentSearches.value))
    } catch (err) {
      console.error('Error saving recent searches:', err)
    }
  }

  // Add a search to recent searches
  const addToRecentSearches = (query) => {
    if (!query) return
    
    // Remove if already exists
    const index = recentSearches.value.indexOf(query)
    if (index !== -1) {
      recentSearches.value.splice(index, 1)
    }
    
    // Add to beginning of array
    recentSearches.value.unshift(query)
    
    // Limit to 5 recent searches
    if (recentSearches.value.length > 5) {
      recentSearches.value = recentSearches.value.slice(0, 5)
    }
    
    saveRecentSearches()
  }

  // Clear recent searches
  const clearRecentSearches = () => {
    recentSearches.value = []
    saveRecentSearches()
  }

  // Perform search
  const search = async (query = null, filters = null) => {
    const searchTerm = query || searchQuery.value
    if (!searchTerm && !filters) return
    
    isSearching.value = true
    searchError.value = null
    
    try {
      // Build query parameters
      const params = new URLSearchParams()
      if (searchTerm) params.append('search', searchTerm)
      
      // Add filters if provided
      const activeFilters = filters || searchFilters.value
      Object.entries(activeFilters).forEach(([key, value]) => {
        if (value !== null && value !== '') {
          params.append(key, value)
        }
      })
      
      const response = await fetch(`${baseURL}/products?${params.toString()}`)
      
      if (!response.ok) {
        throw new Error('Search failed')
      }
      
      const data = await response.json()
      searchResults.value = data.products
      
      // Add to recent searches if it's a text search
      if (searchTerm) {
        addToRecentSearches(searchTerm)
      }
      
      return data
    } catch (err) {
      searchError.value = err.message
      console.error('Search error:', err)
      toast.error('Failed to perform search')
    } finally {
      isSearching.value = false
    }
  }

  // Quick search (for autocomplete)
  const quickSearch = async (query) => {
    if (!query || query.length < 2) return []
    
    try {
      const params = new URLSearchParams()
      params.append('search', query)
      params.append('per_page', 5) // Limit results for quick search
      
      const response = await fetch(`${baseURL}/products?${params.toString()}`)
      
      if (!response.ok) {
        throw new Error('Quick search failed')
      }
      
      const data = await response.json()
      return data.products
    } catch (err) {
      console.error('Quick search error:', err)
      return []
    }
  }

  // Navigate to search results page
  const navigateToSearch = (query = null) => {
    const searchTerm = query || searchQuery.value
    if (!searchTerm) return
    
    // Close search modal if open
    showSearchModal.value = false
    
    // Navigate to search results page with query
    router.push({
      path: '/products',
      query: { search: searchTerm }
    })
  }

  // Clear search
  const clearSearch = () => {
    searchQuery.value = ''
    searchResults.value = []
  }

  // Toggle search modal
  const toggleSearchModal = () => {
    showSearchModal.value = !showSearchModal.value
    if (showSearchModal.value) {
      loadRecentSearches()
    }
  }

  // Reset filters
  const resetFilters = () => {
    searchFilters.value = {
      category: null,
      price_min: null,
      price_max: null,
      material: null,
      occasion: null,
      style: null,
      sort_by: 'relevance'
    }
  }

  // Apply filters
  const applyFilters = async () => {
    await search(searchQuery.value, searchFilters.value)
  }

  // Initialize
  loadRecentSearches()

  return {
    // State
    searchQuery,
    searchResults,
    isSearching,
    searchError,
    recentSearches,
    showSearchModal,
    searchFilters,
    
    // Methods
    search,
    quickSearch,
    navigateToSearch,
    clearSearch,
    toggleSearchModal,
    addToRecentSearches,
    clearRecentSearches,
    resetFilters,
    applyFilters
  }
}