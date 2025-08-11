// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    'nuxt-icon',
    '@nuxtjs/google-fonts',
    '@nuxtjs/color-mode'
  ],

  plugins: [
    '~/plugins/vue-toastification.client.js'
  ],

  css: [
    '~/assets/css/main.css',
    'vue-toastification/dist/index.css'
  ],

  // Configure Google Fonts module
  nuxtGoogleFonts: {
    families: {
      'Playfair+Display': [400, 500, 600, 700],
      'Cinzel': [400, 500, 600, 700],
      'Poppins': [300, 400, 500, 600, 700],
      'Inter': [300, 400, 500, 600, 700]
    },
    display: 'swap',
    prefetch: true,
    preconnect: true
  },

  colorMode: {
    classSuffix: '',
    preference: 'light',
    fallback: 'light'
  },

  app: {
    head: {
      title: 'Nakhrali Fashion - Where Elegance Meets Emotion',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { 
          key: 'description', 
          name: 'description', 
          content: 'Discover exquisite ethnic jewelry at Nakhrali Fashion. Premium gold, silver, and diamond jewelry for every occasion. Bridal, casual, and party wear collections.' 
        },
        { name: 'format-detection', content: 'telephone=no' },
        { property: 'og:title', content: 'Nakhrali Fashion - Luxury Jewelry' },
        { property: 'og:description', content: 'Premium ethnic jewelry collection' },
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'Nakhrali Fashion' },
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Nakhrali Fashion - Luxury Jewelry' },
        { name: 'twitter:description', content: 'Premium ethnic jewelry collection' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000/api',
      appName: 'Nakhrali Fashion',
      appDescription: 'Where Elegance Meets Emotion',
      googleClientId: process.env.GOOGLE_CLIENT_ID || 'your-google-client-id',
      razorpayKey: process.env.RAZORPAY_KEY_ID || 'rzp_test_your_razorpay_key_id',
      shiprocketToken: process.env.SHIPROCKET_TOKEN || 'your-shiprocket-token'
    }
  },

  nitro: {
    devProxy: {
      '/api': {
        target: process.env.API_BASE_URL || 'http://localhost:8000',
        changeOrigin: true
      }
    }
  },
  
  devServer: {
    host: '0.0.0.0',
    port: 3000
  },

  vite: {
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: '@import "@/assets/scss/variables.scss";'
        }
      }
    },
    server: {
      allowedHosts: ['pink-paws-melt.loca.lt', 'thick-bananas-mate.loca.lt']
    }
  },

  // PWA Configuration
  pwa: {
    registerType: 'autoUpdate',
    workbox: {
      navigateFallback: '/',
      globPatterns: ['**/*.{js,css,html,png,svg,ico}']
    },
    client: {
      installPrompt: true
    },
    manifest: {
      name: 'Nakhrali Fashion',
      short_name: 'Nakhrali',
      description: 'Luxury Ethnic Jewelry',
      theme_color: '#B76E79',
      background_color: '#FFFFF0',
      display: 'standalone',
      orientation: 'portrait',
      scope: '/',
      start_url: '/',
      icons: [
        {
          src: '/icon-192.png',
          sizes: '192x192',
          type: 'image/png'
        },
        {
          src: '/icon-512.png',
          sizes: '512x512',
          type: 'image/png'
        }
      ]
    }
  }
})