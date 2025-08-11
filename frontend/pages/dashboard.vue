<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <div class="bg-white shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon">Dashboard</h1>
        <p class="text-gray-600 mt-2">Welcome back, {{ userFullName }}!</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Quick Stats -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 rounded-lg">
              <Icon name="ph:shopping-bag" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Total Orders</p>
              <p class="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 rounded-lg">
              <Icon name="ph:heart" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Wishlist Items</p>
              <p class="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>

        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 bg-rose-gold/10 rounded-lg">
              <Icon name="ph:map-pin" class="w-6 h-6 text-rose-gold" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">Saved Addresses</p>
              <p class="text-2xl font-bold text-gray-900">0</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="mt-8 bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xl font-display text-deep-maroon">Recent Activity</h2>
        </div>
        <div class="p-6">
          <div class="text-center py-8">
            <Icon name="ph:clock" class="w-12 h-12 text-gray-400 mx-auto mb-4" />
            <p class="text-gray-500">No recent activity</p>
            <p class="text-sm text-gray-400 mt-2">Your recent orders and activities will appear here</p>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-8 bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-xl font-display text-deep-maroon">Quick Actions</h2>
        </div>
        <div class="p-6">
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <NuxtLink
              to="/products"
              class="flex items-center p-4 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors"
            >
              <Icon name="ph:shopping-bag" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium">Shop Now</span>
            </NuxtLink>

            <NuxtLink
              to="/account"
              class="flex items-center p-4 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors"
            >
              <Icon name="ph:user" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium">My Profile</span>
            </NuxtLink>

            <NuxtLink
              to="/orders"
              class="flex items-center p-4 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors"
            >
              <Icon name="ph:package" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium">My Orders</span>
            </NuxtLink>

            <NuxtLink
              to="/wishlist"
              class="flex items-center p-4 border border-gray-200 rounded-lg hover:border-rose-gold hover:bg-rose-gold/5 transition-colors"
            >
              <Icon name="ph:heart" class="w-5 h-5 text-rose-gold mr-3" />
              <span class="font-medium">Wishlist</span>
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Dashboard - Nakhrali Fashion',
  meta: [
    {
      name: 'description',
      content: 'Your Nakhrali Fashion dashboard - manage your account, view orders, and explore our jewelry collections.'
    }
  ]
})

const { user, userFullName } = useAuth()

// Apply auth middleware
definePageMeta({
  middleware: 'auth'
})
</script> 