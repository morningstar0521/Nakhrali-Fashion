<template>
  <div class="container mx-auto px-4 py-12">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-display text-center mb-12">Contact Us</h1>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Contact Form -->
        <div class="bg-white rounded-lg shadow-md p-8">
          <h2 class="text-2xl font-display mb-6">Send Us a Message</h2>
          
          <form @submit.prevent="submitForm" class="space-y-4">
            <div>
              <label for="name" class="block text-gray-700 mb-1">Your Name</label>
              <input 
                type="text" 
                id="name" 
                v-model="form.name" 
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold/50"
                required
              >
            </div>
            
            <div>
              <label for="email" class="block text-gray-700 mb-1">Email Address</label>
              <input 
                type="email" 
                id="email" 
                v-model="form.email" 
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold/50"
                required
              >
            </div>
            
            <div>
              <label for="subject" class="block text-gray-700 mb-1">Subject</label>
              <input 
                type="text" 
                id="subject" 
                v-model="form.subject" 
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold/50"
                required
              >
            </div>
            
            <div>
              <label for="message" class="block text-gray-700 mb-1">Your Message</label>
              <textarea 
                id="message" 
                v-model="form.message" 
                rows="5"
                class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-rose-gold/50"
                required
              ></textarea>
            </div>
            
            <button 
              type="submit" 
              class="bg-rose-gold text-white font-medium py-2 px-6 rounded-md hover:bg-rose-gold/90 transition-colors w-full"
              :disabled="isSubmitting"
            >
              {{ isSubmitting ? 'Sending...' : 'Send Message' }}
            </button>
          </form>
        </div>
        
        <!-- Contact Information -->
        <div>
          <div class="bg-white rounded-lg shadow-md p-8 mb-8">
            <h2 class="text-2xl font-display mb-6">Contact Information</h2>
            
            <div class="space-y-4">
              <div class="flex items-start">
                <Icon name="mdi:map-marker" class="w-6 h-6 text-rose-gold mr-3 mt-1" />
                <div>
                  <h3 class="font-medium">Address</h3>
                  <p class="text-gray-700">
                    123 Fashion Street, Jewelry Lane<br>
                    Mumbai, Maharashtra 400001<br>
                    India
                  </p>
                </div>
              </div>
              
              <div class="flex items-start">
                <Icon name="mdi:phone" class="w-6 h-6 text-rose-gold mr-3 mt-1" />
                <div>
                  <h3 class="font-medium">Phone</h3>
                  <p class="text-gray-700">
                    +91 98765 43210<br>
                    +91 12345 67890
                  </p>
                </div>
              </div>
              
              <div class="flex items-start">
                <Icon name="mdi:email" class="w-6 h-6 text-rose-gold mr-3 mt-1" />
                <div>
                  <h3 class="font-medium">Email</h3>
                  <p class="text-gray-700">
                    info@nakhralifashion.com<br>
                    support@nakhralifashion.com
                  </p>
                </div>
              </div>
              
              <div class="flex items-start">
                <Icon name="mdi:clock" class="w-6 h-6 text-rose-gold mr-3 mt-1" />
                <div>
                  <h3 class="font-medium">Business Hours</h3>
                  <p class="text-gray-700">
                    Monday - Saturday: 10:00 AM - 8:00 PM<br>
                    Sunday: 11:00 AM - 6:00 PM
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-8">
            <h2 class="text-2xl font-display mb-6">Connect With Us</h2>
            
            <div class="flex space-x-4">
              <a href="#" class="text-gray-700 hover:text-rose-gold transition-colors">
                <Icon name="mdi:facebook" class="w-8 h-8" />
              </a>
              <a href="#" class="text-gray-700 hover:text-rose-gold transition-colors">
                <Icon name="mdi:instagram" class="w-8 h-8" />
              </a>
              <a href="#" class="text-gray-700 hover:text-rose-gold transition-colors">
                <Icon name="mdi:twitter" class="w-8 h-8" />
              </a>
              <a href="#" class="text-gray-700 hover:text-rose-gold transition-colors">
                <Icon name="mdi:pinterest" class="w-8 h-8" />
              </a>
              <a href="#" class="text-gray-700 hover:text-rose-gold transition-colors">
                <Icon name="mdi:youtube" class="w-8 h-8" />
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useToast } from 'vue-toastification';

definePageMeta({
  title: 'Contact Us - Nakhrali Fashion',
  description: 'Get in touch with Nakhrali Fashion for any queries or feedback'
});

const toast = useToast();

const form = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
});

const isSubmitting = ref(false);

const submitForm = async () => {
  isSubmitting.value = true;
  
  try {
    // In a real application, you would send this data to your backend API
    // await $fetch('/api/contact', {
    //   method: 'POST',
    //   body: form.value
    // });
    
    // For now, we'll just simulate a successful submission
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    toast.success('Your message has been sent successfully!');
    
    // Reset form
    form.value = {
      name: '',
      email: '',
      subject: '',
      message: ''
    };
  } catch (error) {
    toast.error('There was an error sending your message. Please try again.');
    console.error('Contact form submission error:', error);
  } finally {
    isSubmitting.value = false;
  }
};
</script>