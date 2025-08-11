<template>
  <div class="min-h-screen bg-gradient-to-br from-ivory to-rose-gold/10 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-md">
      <h1 class="text-3xl font-display font-bold text-deep-maroon mb-8">Size Guide</h1>
      
      <div class="space-y-8">
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Ring Size Guide</h2>
          
          <div class="prose prose-rose max-w-none text-gray-600 mb-6">
            <p>Finding your perfect ring size is essential for comfort and security. Use the chart below to determine your ring size, or request our free ring sizer tool for precise measurements at home.</p>
          </div>
          
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">US Size</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">UK Size</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">EU Size</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Diameter (mm)</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Circumference (mm)</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(size, index) in ringSizes" :key="index">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ size.us }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.uk }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.eu }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.diameter }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.circumference }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          
          <div class="mt-6 p-4 bg-rose-gold/10 rounded-lg border border-rose-gold/20">
            <h3 class="text-lg font-medium text-deep-maroon mb-2">How to Measure Your Ring Size at Home</h3>
            <ol class="list-decimal list-inside space-y-2 text-gray-600">
              <li>Wrap a piece of string or paper around your finger where you would wear the ring.</li>
              <li>Mark the point where the string or paper meets.</li>
              <li>Measure the length in millimeters.</li>
              <li>Use the circumference measurement in the chart above to find your size.</li>
            </ol>
            <p class="mt-4 text-sm text-gray-600">For the most accurate measurement, measure your finger at the end of the day when your fingers are at their largest. Avoid measuring when your hands are cold, as fingers tend to be smaller.</p>
          </div>
        </section>
        
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Bracelet Size Guide</h2>
          
          <div class="prose prose-rose max-w-none text-gray-600 mb-6">
            <p>To find your perfect bracelet size, measure your wrist circumference and add 1-2 cm for a comfortable fit.</p>
          </div>
          
          <div class="overflow-x-auto">
            <table class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Size</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Wrist Circumference (cm)</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Bracelet Length (cm)</th>
                  <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Fit</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="(size, index) in braceletSizes" :key="index">
                  <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ size.size }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.wrist }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.length }}</td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.fit }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
        
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Necklace Length Guide</h2>
          
          <div class="prose prose-rose max-w-none text-gray-600 mb-6">
            <p>Necklace lengths vary by style. Use this guide to find the perfect length for your desired look.</p>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                  <thead class="bg-gray-50">
                    <tr>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Style</th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Length (inches)</th>
                      <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Length (cm)</th>
                    </tr>
                  </thead>
                  <tbody class="bg-white divide-y divide-gray-200">
                    <tr v-for="(size, index) in necklaceSizes" :key="index">
                      <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">{{ size.style }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.inches }}</td>
                      <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{{ size.cm }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            
            <div class="flex items-center justify-center">
              <img src="/images/necklace-length-guide.svg" alt="Necklace Length Guide" class="max-w-full h-auto max-h-80" />
            </div>
          </div>
        </section>
        
        <section>
          <h2 class="text-2xl font-display font-semibold text-deep-maroon mb-4">Need More Help?</h2>
          
          <div class="bg-gray-50 p-6 rounded-lg">
            <p class="text-gray-600 mb-4">If you're unsure about your size or have specific questions, our jewelry experts are here to help.</p>
            
            <div class="flex flex-col sm:flex-row sm:space-x-4">
              <a href="/help" class="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-rose-gold hover:bg-deep-maroon focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold mb-3 sm:mb-0">
                <Icon name="ph:question" class="-ml-1 mr-2 h-5 w-5" />
                Contact Customer Service
              </a>
              
              <button class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
                <Icon name="ph:ruler" class="-ml-1 mr-2 h-5 w-5" />
                Request Free Ring Sizer
              </button>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const ringSizes = ref([
  { us: '3', uk: 'F', eu: '44', diameter: '14.1', circumference: '44.2' },
  { us: '4', uk: 'H', eu: '47', diameter: '14.8', circumference: '46.5' },
  { us: '5', uk: 'J', eu: '49', diameter: '15.7', circumference: '49.3' },
  { us: '6', uk: 'L', eu: '52', diameter: '16.5', circumference: '51.9' },
  { us: '7', uk: 'N', eu: '54', diameter: '17.3', circumference: '54.4' },
  { us: '8', uk: 'P', eu: '57', diameter: '18.1', circumference: '56.9' },
  { us: '9', uk: 'R', eu: '59', diameter: '18.9', circumference: '59.5' },
  { us: '10', uk: 'T', eu: '62', diameter: '19.8', circumference: '62.1' },
  { us: '11', uk: 'V', eu: '64', diameter: '20.6', circumference: '64.6' },
  { us: '12', uk: 'X', eu: '67', diameter: '21.4', circumference: '67.2' }
]);

const braceletSizes = ref([
  { size: 'XS', wrist: '13-14', length: '15-16', fit: 'Snug' },
  { size: 'S', wrist: '15-16', length: '17-18', fit: 'Comfort' },
  { size: 'M', wrist: '17-18', length: '19-20', fit: 'Comfort' },
  { size: 'L', wrist: '19-20', length: '21-22', fit: 'Comfort' },
  { size: 'XL', wrist: '21-22', length: '23-24', fit: 'Comfort' }
]);

const necklaceSizes = ref([
  { style: 'Choker', inches: '14-16', cm: '35-41' },
  { style: 'Princess', inches: '18', cm: '45' },
  { style: 'Matinee', inches: '20-22', cm: '50-56' },
  { style: 'Opera', inches: '24-30', cm: '61-76' },
  { style: 'Rope', inches: '36+', cm: '91+' }
]);
</script>