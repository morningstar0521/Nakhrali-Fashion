<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Header -->
    <div class="bg-white dark:bg-gray-800 shadow">
      <div class="container mx-auto px-4 py-6">
        <h1 class="text-3xl font-display text-deep-maroon dark:text-rose-gold">Site Settings</h1>
        <p class="text-gray-600 dark:text-gray-400 mt-2">Configure your store settings and preferences</p>
      </div>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <!-- Settings Navigation -->
        <div class="lg:col-span-1">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
            <div class="p-4 border-b border-gray-200 dark:border-gray-700">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white">Settings</h3>
            </div>
            <nav class="space-y-1 p-2">
              <button 
                v-for="(section, index) in settingSections" 
                :key="index"
                @click="activeSection = section.id"
                class="w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors" 
                :class="activeSection === section.id ? 'bg-rose-gold/10 text-deep-maroon dark:text-rose-gold' : 'text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700'"
              >
                <Icon :name="section.icon" class="mr-3 h-5 w-5" />
                {{ section.name }}
              </button>
            </nav>
          </div>
        </div>

        <!-- Settings Content -->
        <div class="lg:col-span-3">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow">
            <!-- General Settings -->
            <div v-if="activeSection === 'general'" class="p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">General Settings</h3>
              
              <div class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Store Name</label>
                  <input 
                    type="text" 
                    v-model="settings.general.storeName" 
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Store Email</label>
                  <input 
                    type="email" 
                    v-model="settings.general.storeEmail" 
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Store Phone</label>
                  <input 
                    type="tel" 
                    v-model="settings.general.storePhone" 
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  />
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Store Address</label>
                  <textarea 
                    v-model="settings.general.storeAddress" 
                    rows="3"
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  ></textarea>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency</label>
                  <select 
                    v-model="settings.general.currency" 
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  >
                    <option value="INR">Indian Rupee (₹)</option>
                    <option value="USD">US Dollar ($)</option>
                    <option value="EUR">Euro (€)</option>
                    <option value="GBP">British Pound (£)</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Default Language</label>
                  <select 
                    v-model="settings.general.language" 
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  >
                    <option value="en">English</option>
                    <option value="hi">Hindi</option>
                    <option value="bn">Bengali</option>
                    <option value="ta">Tamil</option>
                    <option value="te">Telugu</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Appearance Settings -->
            <div v-if="activeSection === 'appearance'" class="p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">Appearance Settings</h3>
              
              <div class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Theme</label>
                  <div class="grid grid-cols-3 gap-4 mt-2">
                    <div 
                      v-for="theme in themes" 
                      :key="theme.id"
                      @click="settings.appearance.theme = theme.id"
                      class="border rounded-lg overflow-hidden cursor-pointer transition-all" 
                      :class="settings.appearance.theme === theme.id ? 'ring-2 ring-rose-gold' : 'hover:shadow-md'"
                    >
                      <div class="h-24 bg-gray-200 dark:bg-gray-700">
                        <img :src="theme.thumbnail" :alt="theme.name" class="w-full h-full object-cover" />
                      </div>
                      <div class="p-2 text-center">
                        <p class="text-sm font-medium text-gray-900 dark:text-white">{{ theme.name }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Color Scheme</label>
                  <div class="flex flex-wrap gap-3 mt-2">
                    <div 
                      v-for="color in colorSchemes" 
                      :key="color.id"
                      @click="settings.appearance.colorScheme = color.id"
                      class="w-8 h-8 rounded-full cursor-pointer transition-transform hover:scale-110" 
                      :style="{ backgroundColor: color.value }"
                      :class="settings.appearance.colorScheme === color.id ? 'ring-2 ring-offset-2 ring-gray-400' : ''"
                    ></div>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Logo</label>
                  <div class="mt-2 flex items-center">
                    <div class="h-16 w-16 overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                      <img v-if="settings.appearance.logo" :src="settings.appearance.logo" alt="Store Logo" class="h-full w-full object-contain" />
                      <Icon v-else name="ph:image" class="h-8 w-8 text-gray-400" />
                    </div>
                    <button class="ml-5 bg-white dark:bg-gray-700 py-2 px-3 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
                      Change
                    </button>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Favicon</label>
                  <div class="mt-2 flex items-center">
                    <div class="h-10 w-10 overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-700 flex items-center justify-center">
                      <img v-if="settings.appearance.favicon" :src="settings.appearance.favicon" alt="Favicon" class="h-full w-full object-contain" />
                      <Icon v-else name="ph:image" class="h-6 w-6 text-gray-400" />
                    </div>
                    <button class="ml-5 bg-white dark:bg-gray-700 py-2 px-3 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-gold">
                      Change
                    </button>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Enable Dark Mode</label>
                  <div class="mt-2">
                    <label class="inline-flex items-center">
                      <input type="checkbox" v-model="settings.appearance.enableDarkMode" class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold" />
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Allow users to switch to dark mode</span>
                    </label>
                  </div>
                </div>
              </div>
            </div>

            <!-- Payment Settings -->
            <div v-if="activeSection === 'payment'" class="p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">Payment Settings</h3>
              
              <div class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Currency Format</label>
                  <select 
                    v-model="settings.payment.currencyFormat" 
                    class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                  >
                    <option value="symbol_first">Symbol First (₹1,000.00)</option>
                    <option value="symbol_last">Symbol Last (1,000.00₹)</option>
                    <option value="code_first">Code First (INR 1,000.00)</option>
                  </select>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Enabled Payment Methods</label>
                  <div class="mt-2 space-y-2">
                    <label v-for="method in paymentMethods" :key="method.id" class="flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="settings.payment.enabledMethods" 
                        :value="method.id" 
                        class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                      />
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">{{ method.name }}</span>
                    </label>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Razorpay Settings</label>
                  <div class="mt-2 space-y-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">API Key</label>
                      <input 
                        type="text" 
                        v-model="settings.payment.razorpay.apiKey" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Secret Key</label>
                      <input 
                        type="password" 
                        v-model="settings.payment.razorpay.secretKey" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Webhook Secret</label>
                      <input 
                        type="password" 
                        v-model="settings.payment.razorpay.webhookSecret" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">PayPal Settings</label>
                  <div class="mt-2 space-y-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Client ID</label>
                      <input 
                        type="text" 
                        v-model="settings.payment.paypal.clientId" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Secret</label>
                      <input 
                        type="password" 
                        v-model="settings.payment.paypal.secret" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label class="inline-flex items-center">
                        <input 
                          type="checkbox" 
                          v-model="settings.payment.paypal.sandboxMode" 
                          class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                        />
                        <span class="ml-2 text-xs text-gray-500 dark:text-gray-400">Sandbox Mode</span>
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Shipping Settings -->
            <div v-if="activeSection === 'shipping'" class="p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">Shipping Settings</h3>
              
              <div class="space-y-6">
                <div>
                  <div class="flex items-center justify-between">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Shipping Zones</label>
                    <button 
                      @click="addShippingZone" 
                      class="text-sm text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 flex items-center"
                    >
                      <Icon name="ph:plus-circle" class="h-4 w-4 mr-1" />
                      Add Zone
                    </button>
                  </div>
                  
                  <div class="mt-2 space-y-4">
                    <div 
                      v-for="(zone, index) in settings.shipping.zones" 
                      :key="index" 
                      class="border border-gray-200 dark:border-gray-700 rounded-lg p-4"
                    >
                      <div class="flex justify-between items-start mb-3">
                        <div>
                          <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ zone.name }}</h4>
                          <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ zone.countries.join(', ') }}</p>
                        </div>
                        <button @click="removeShippingZone(index)" class="text-gray-400 hover:text-red-500">
                          <Icon name="ph:trash" class="h-5 w-5" />
                        </button>
                      </div>
                      
                      <div class="space-y-3">
                        <div class="grid grid-cols-3 gap-3">
                          <div>
                            <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Method</label>
                            <input 
                              type="text" 
                              v-model="zone.method" 
                              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                              placeholder="Standard Shipping"
                            />
                          </div>
                          <div>
                            <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Cost</label>
                            <input 
                              type="number" 
                              v-model="zone.cost" 
                              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                              placeholder="100"
                            />
                          </div>
                          <div>
                            <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Free Above</label>
                            <input 
                              type="number" 
                              v-model="zone.freeAbove" 
                              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                              placeholder="1000"
                            />
                          </div>
                        </div>
                        
                        <div>
                          <label class="inline-flex items-center">
                            <input 
                              type="checkbox" 
                              v-model="zone.enabled" 
                              class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                            />
                            <span class="ml-2 text-xs text-gray-700 dark:text-gray-300">Enabled</span>
                          </label>
                        </div>
                      </div>
                    </div>
                    
                    <div v-if="settings.shipping.zones.length === 0" class="text-center py-4 text-gray-500 dark:text-gray-400 text-sm">
                      No shipping zones defined. Click "Add Zone" to create one.
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Shipping Options</label>
                  <div class="mt-2 space-y-2">
                    <label class="flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="settings.shipping.enableLocalPickup" 
                        class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                      />
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Enable Local Pickup</span>
                    </label>
                    
                    <label class="flex items-center">
                      <input 
                        type="checkbox" 
                        v-model="settings.shipping.enableFreeShipping" 
                        class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                      />
                      <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Enable Free Shipping</span>
                    </label>
                    
                    <div v-if="settings.shipping.enableFreeShipping" class="ml-6 mt-2">
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Minimum Order Amount for Free Shipping</label>
                      <input 
                        type="number" 
                        v-model="settings.shipping.freeShippingMinimum" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Email Settings -->
            <div v-if="activeSection === 'email'" class="p-6">
              <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-6">Email Settings</h3>
              
              <div class="space-y-6">
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">SMTP Configuration</label>
                  <div class="mt-2 space-y-3 p-3 border border-gray-200 dark:border-gray-700 rounded-lg">
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">SMTP Host</label>
                      <input 
                        type="text" 
                        v-model="settings.email.smtp.host" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                        placeholder="smtp.example.com"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">SMTP Port</label>
                      <input 
                        type="number" 
                        v-model="settings.email.smtp.port" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                        placeholder="587"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Username</label>
                      <input 
                        type="text" 
                        v-model="settings.email.smtp.username" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                        placeholder="user@example.com"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Password</label>
                      <input 
                        type="password" 
                        v-model="settings.email.smtp.password" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      />
                    </div>
                    <div>
                      <label class="block text-xs text-gray-500 dark:text-gray-400 mb-1">Encryption</label>
                      <select 
                        v-model="settings.email.smtp.encryption" 
                        class="w-full px-3 py-2 border border-gray-300 dark:border-gray-700 rounded-lg focus:ring-2 focus:ring-rose-gold focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                      >
                        <option value="tls">TLS</option>
                        <option value="ssl">SSL</option>
                        <option value="none">None</option>
                      </select>
                    </div>
                    <div>
                      <label class="inline-flex items-center">
                        <input 
                          type="checkbox" 
                          v-model="settings.email.smtp.enabled" 
                          class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                        />
                        <span class="ml-2 text-xs text-gray-700 dark:text-gray-300">Enable SMTP</span>
                      </label>
                    </div>
                  </div>
                </div>
                
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Email Templates</label>
                  <div class="mt-2 space-y-3">
                    <div v-for="template in emailTemplates" :key="template.id" class="border border-gray-200 dark:border-gray-700 rounded-lg p-4">
                      <div class="flex justify-between items-center mb-3">
                        <h4 class="text-sm font-medium text-gray-900 dark:text-white">{{ template.name }}</h4>
                        <button class="text-rose-gold hover:text-deep-maroon dark:hover:text-rose-gold/80 text-sm">
                          Edit Template
                        </button>
                      </div>
                      <p class="text-xs text-gray-500 dark:text-gray-400">{{ template.description }}</p>
                      <div class="mt-2">
                        <label class="inline-flex items-center">
                          <input 
                            type="checkbox" 
                            v-model="settings.email.enabledTemplates" 
                            :value="template.id" 
                            class="rounded border-gray-300 text-rose-gold focus:ring-rose-gold"
                          />
                          <span class="ml-2 text-xs text-gray-700 dark:text-gray-300">Enabled</span>
                        </label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Save Button -->
            <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 flex justify-end">
              <button 
                @click="saveSettings" 
                class="px-4 py-2 bg-rose-gold hover:bg-deep-maroon text-white rounded-lg flex items-center"
              >
                <Icon name="ph:floppy-disk" class="mr-2 h-5 w-5" />
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// SEO
useHead({
  title: 'Site Settings - Nakhrali Fashion Admin',
  meta: [
    {
      name: 'description',
      content: 'Configure site settings for Nakhrali Fashion.'
    }
  ]
})

// Auth
const { isAdmin } = useAuth()

// Apply admin middleware
definePageMeta({
  middleware: 'admin'
})

// State
const activeSection = ref('general')

// Setting sections
const settingSections = [
  { id: 'general', name: 'General', icon: 'ph:gear' },
  { id: 'appearance', name: 'Appearance', icon: 'ph:paint-brush' },
  { id: 'payment', name: 'Payment', icon: 'ph:credit-card' },
  { id: 'shipping', name: 'Shipping', icon: 'ph:truck' },
  { id: 'email', name: 'Email', icon: 'ph:envelope' },
]

// Mock data for settings
const settings = ref({
  general: {
    storeName: 'Nakhrali Fashion',
    storeEmail: 'info@nakhrali.com',
    storePhone: '+91 98765 43210',
    storeAddress: '123 Fashion Street, Mumbai, Maharashtra 400001, India',
    currency: 'INR',
    language: 'en',
  },
  appearance: {
    theme: 'classic',
    colorScheme: 'rose-gold',
    logo: 'https://placehold.co/200x80?text=Nakhrali+Fashion',
    favicon: 'https://placehold.co/32x32?text=NF',
    enableDarkMode: true,
  },
  payment: {
    currencyFormat: 'symbol_first',
    enabledMethods: ['razorpay', 'paypal', 'cod'],
    razorpay: {
      apiKey: 'rzp_test_xxxxxxxxxxxxxxx',
      secretKey: '••••••••••••••••••••••••',
      webhookSecret: '••••••••••••••••••••••••',
    },
    paypal: {
      clientId: 'test_xxxxxxxxxxxxxxx',
      secret: '••••••••••••••••••••••••',
      sandboxMode: true,
    },
  },
  shipping: {
    zones: [
      {
        name: 'India',
        countries: ['India'],
        method: 'Standard Shipping',
        cost: 100,
        freeAbove: 1000,
        enabled: true,
      },
      {
        name: 'International',
        countries: ['United States', 'United Kingdom', 'Canada', 'Australia'],
        method: 'International Shipping',
        cost: 1500,
        freeAbove: 10000,
        enabled: true,
      },
    ],
    enableLocalPickup: true,
    enableFreeShipping: true,
    freeShippingMinimum: 1000,
  },
  email: {
    smtp: {
      host: 'smtp.gmail.com',
      port: 587,
      username: 'info@nakhrali.com',
      password: '••••••••••••••••',
      encryption: 'tls',
      enabled: true,
    },
    enabledTemplates: ['order_confirmation', 'shipping_confirmation', 'account_welcome'],
  },
})

// Themes
const themes = [
  { id: 'classic', name: 'Classic', thumbnail: 'https://placehold.co/300x200?text=Classic+Theme' },
  { id: 'modern', name: 'Modern', thumbnail: 'https://placehold.co/300x200?text=Modern+Theme' },
  { id: 'minimal', name: 'Minimal', thumbnail: 'https://placehold.co/300x200?text=Minimal+Theme' },
]

// Color schemes
const colorSchemes = [
  { id: 'rose-gold', name: 'Rose Gold', value: '#bd8c7d' },
  { id: 'deep-maroon', name: 'Deep Maroon', value: '#800020' },
  { id: 'royal-blue', name: 'Royal Blue', value: '#4169e1' },
  { id: 'emerald', name: 'Emerald', value: '#50c878' },
  { id: 'purple', name: 'Purple', value: '#800080' },
  { id: 'teal', name: 'Teal', value: '#008080' },
]

// Payment methods
const paymentMethods = [
  { id: 'razorpay', name: 'Razorpay' },
  { id: 'paypal', name: 'PayPal' },
  { id: 'stripe', name: 'Stripe' },
  { id: 'cod', name: 'Cash on Delivery' },
  { id: 'bank_transfer', name: 'Bank Transfer' },
]

// Email templates
const emailTemplates = [
  { 
    id: 'order_confirmation', 
    name: 'Order Confirmation', 
    description: 'Sent to customers when they place an order.' 
  },
  { 
    id: 'shipping_confirmation', 
    name: 'Shipping Confirmation', 
    description: 'Sent to customers when their order ships.' 
  },
  { 
    id: 'account_welcome', 
    name: 'Welcome Email', 
    description: 'Sent to customers when they create an account.' 
  },
  { 
    id: 'password_reset', 
    name: 'Password Reset', 
    description: 'Sent to customers when they request a password reset.' 
  },
  { 
    id: 'abandoned_cart', 
    name: 'Abandoned Cart', 
    description: 'Sent to customers who abandon their shopping cart.' 
  },
]

// Methods
const addShippingZone = () => {
  settings.value.shipping.zones.push({
    name: 'New Zone',
    countries: [''],
    method: 'Standard Shipping',
    cost: 0,
    freeAbove: 0,
    enabled: true,
  })
}

const removeShippingZone = (index) => {
  settings.value.shipping.zones.splice(index, 1)
}

const saveSettings = () => {
  // In a real application, this would be an API call
  alert('Settings saved successfully!')
}
</script>