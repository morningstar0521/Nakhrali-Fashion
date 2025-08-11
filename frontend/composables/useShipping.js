import { ref, readonly } from 'vue'
import { useAuth } from './useAuth'

export const useShipping = () => {
  const config = useRuntimeConfig()
  const { accessToken } = useAuth()
  
  // State
  const isLoading = ref(false)
  const error = ref(null)
  const trackingInfo = ref(null)
  
  // Get tracking information for an order
  const getTrackingInfo = async (orderId) => {
    isLoading.value = true
    error.value = null
    
    try {
      // This would be an API call to your backend, which would then call Shiprocket API
      const response = await $fetch(`${config.public.apiBase}/shipping/track/${orderId}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        }
      })
      
      trackingInfo.value = response
      return response
    } catch (err) {
      console.error('Error fetching tracking info:', err)
      error.value = 'Failed to fetch tracking information'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Generate shipping label
  const generateShippingLabel = async (orderId) => {
    isLoading.value = true
    error.value = null
    
    try {
      // This would be an API call to your backend, which would then call Shiprocket API
      const response = await $fetch(`${config.public.apiBase}/shipping/label/${orderId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        }
      })
      
      return response.label_url
    } catch (err) {
      console.error('Error generating shipping label:', err)
      error.value = 'Failed to generate shipping label'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Calculate shipping rates
  const calculateShippingRates = async (pincode, weight, cod = false) => {
    isLoading.value = true
    error.value = null
    
    try {
      // This would be an API call to your backend, which would then call Shiprocket API
      const response = await $fetch(`${config.public.apiBase}/shipping/rates`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: {
          pickup_postcode: '400001', // Your warehouse pincode
          delivery_postcode: pincode,
          weight, // in kg
          cod
        }
      })
      
      return response.available_courier_companies
    } catch (err) {
      console.error('Error calculating shipping rates:', err)
      error.value = 'Failed to calculate shipping rates'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  // Check delivery serviceability
  const checkServiceability = async (pincode) => {
    isLoading.value = true
    error.value = null
    
    try {
      // This would be an API call to your backend, which would then call Shiprocket API
      const response = await $fetch(`${config.public.apiBase}/shipping/serviceability`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${accessToken.value}`
        },
        body: {
          pickup_postcode: '400001', // Your warehouse pincode
          delivery_postcode: pincode
        }
      })
      
      return {
        serviceable: response.is_serviceable,
        estimatedDeliveryDays: response.estimated_delivery_days
      }
    } catch (err) {
      console.error('Error checking serviceability:', err)
      error.value = 'Failed to check delivery serviceability'
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  return {
    isLoading: readonly(isLoading),
    error: readonly(error),
    trackingInfo: readonly(trackingInfo),
    getTrackingInfo,
    generateShippingLabel,
    calculateShippingRates,
    checkServiceability
  }
}