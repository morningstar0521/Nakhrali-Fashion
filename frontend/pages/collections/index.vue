<template>
  <div class="container mx-auto px-4 py-12">
    <h1 class="text-4xl font-display text-center mb-12">Our Collections</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <!-- Festive Collection -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
        <div class="h-64 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20 relative">
          <div class="absolute inset-0 flex items-center justify-center">
            <h3 class="text-3xl font-display text-gray-900">Festive Collection</h3>
          </div>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Celebrate special occasions with our stunning festive jewelry collection.</p>
          <NuxtLink to="/products?collection=festive" class="btn-primary w-full text-center py-2">
            Explore Collection
          </NuxtLink>
        </div>
      </div>
      
      <!-- Office Wear -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
        <div class="h-64 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20 relative">
          <div class="absolute inset-0 flex items-center justify-center">
            <h3 class="text-3xl font-display text-gray-900">Office Wear</h3>
          </div>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Elegant and professional jewelry perfect for your workplace attire.</p>
          <NuxtLink to="/products?collection=office" class="btn-primary w-full text-center py-2">
            Explore Collection
          </NuxtLink>
        </div>
      </div>
      
      <!-- Gifting -->
      <div class="bg-white rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
        <div class="h-64 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20 relative">
          <div class="absolute inset-0 flex items-center justify-center">
            <h3 class="text-3xl font-display text-gray-900">Gifting</h3>
          </div>
        </div>
        <div class="p-6">
          <p class="text-gray-600 mb-4">Perfect gift options for your loved ones on special occasions.</p>
          <NuxtLink to="/products?collection=gifting" class="btn-primary w-full text-center py-2">
            Explore Collection
          </NuxtLink>
        </div>
      </div>
    </div>
    
    <div class="mt-16">
      <h2 class="text-3xl font-display text-center mb-8">Shop by Category</h2>
      
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <!-- Categories -->
        <NuxtLink to="/products?category=rings" class="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
          <div class="h-20 flex items-center justify-center">
            <Icon name="mdi:ring" class="w-12 h-12 text-rose-gold" />
          </div>
          <p class="font-medium">Rings</p>
        </NuxtLink>
        
        <NuxtLink to="/products?category=earrings" class="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
          <div class="h-20 flex items-center justify-center">
            <Icon name="mdi:earring" class="w-12 h-12 text-rose-gold" />
          </div>
          <p class="font-medium">Earrings</p>
        </NuxtLink>
        
        <NuxtLink to="/products?category=necklaces" class="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
          <div class="h-20 flex items-center justify-center">
            <Icon name="mdi:necklace" class="w-12 h-12 text-rose-gold" />
          </div>
          <p class="font-medium">Necklaces</p>
        </NuxtLink>
        
        <NuxtLink to="/products?category=bangles" class="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
          <div class="h-20 flex items-center justify-center">
            <Icon name="mdi:bracelet" class="w-12 h-12 text-rose-gold" />
          </div>
          <p class="font-medium">Bangles</p>
        </NuxtLink>
        
        <NuxtLink to="/products?category=bracelets" class="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
          <div class="h-20 flex items-center justify-center">
            <Icon name="mdi:bracelet" class="w-12 h-12 text-rose-gold" />
          </div>
          <p class="font-medium">Bracelets</p>
        </NuxtLink>
        
        <NuxtLink to="/products?category=bridal" class="bg-white rounded-lg p-4 text-center shadow-sm hover:shadow-md transition-shadow">
          <div class="h-20 flex items-center justify-center">
            <Icon name="mdi:crown" class="w-12 h-12 text-rose-gold" />
          </div>
          <p class="font-medium">Bridal</p>
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'Collections - Nakhrali Fashion',
  description: 'Explore our exquisite collections of ethnic jewelry at Nakhrali Fashion'
});
</script>

<style scoped>
.btn-primary {
  @apply bg-rose-gold text-white font-medium rounded-md hover:bg-rose-gold/90 transition-colors;
}
</style>