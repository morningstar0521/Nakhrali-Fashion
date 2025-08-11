<template>
  <div class="container mx-auto px-4 py-12">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-4xl font-display text-center mb-12">About Nakhrali Fashion</h1>
      
      <!-- Our Story Section -->
      <section class="mb-16">
        <h2 class="text-3xl font-display mb-6">Our Story</h2>
        <div class="bg-white rounded-lg shadow-md p-8">
          <p class="text-gray-700 mb-4">
            Nakhrali Fashion was born out of a passion for preserving and celebrating the rich heritage of Indian jewelry craftsmanship. Founded in 2018, our journey began with a simple mission: to create exquisite ethnic jewelry that tells a story and connects the wearer to centuries of tradition.
          </p>
          <p class="text-gray-700 mb-4">
            Our founder, Priya Sharma, grew up watching her grandmother's collection of heirloom jewelry pieces that had been passed down through generations. Inspired by these treasures and the stories they carried, she set out to create a brand that would honor traditional techniques while embracing contemporary design sensibilities.
          </p>
          <p class="text-gray-700">
            Today, Nakhrali Fashion stands as a testament to that vision, offering handcrafted jewelry that bridges the gap between tradition and modernity, between the past and the present.
          </p>
        </div>
      </section>
      
      <!-- Our Craftsmanship Section -->
      <section class="mb-16">
        <h2 class="text-3xl font-display mb-6">Our Craftsmanship</h2>
        <div class="bg-white rounded-lg shadow-md p-8">
          <p class="text-gray-700 mb-4">
            At Nakhrali Fashion, we believe that true luxury lies in the details. Each piece in our collection is meticulously handcrafted by skilled artisans who have inherited their craft through generations. We work closely with these artisans, ensuring fair wages and ethical working conditions while preserving their invaluable skills.
          </p>
          <p class="text-gray-700 mb-4">
            We source only the finest materials – from ethically mined gemstones to high-quality metals – to create jewelry that not only looks beautiful but is built to last. Our commitment to quality means that each piece undergoes rigorous quality checks before it reaches you.
          </p>
          <p class="text-gray-700">
            From intricate meenakari work to delicate kundan settings, from traditional polki to contemporary fusion designs, our collections showcase the diverse techniques that make Indian jewelry so unique and coveted around the world.
          </p>
        </div>
      </section>
      
      <!-- Our Values Section -->
      <section class="mb-16">
        <h2 class="text-3xl font-display mb-6">Our Values</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white rounded-lg shadow-md p-6 text-center">
            <div class="h-16 flex items-center justify-center mb-4">
              <Icon name="mdi:hand-heart" class="w-12 h-12 text-rose-gold" />
            </div>
            <h3 class="text-xl font-display mb-2">Ethical Sourcing</h3>
            <p class="text-gray-700">
              We ensure all our materials are ethically sourced and our artisans are fairly compensated.
            </p>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6 text-center">
            <div class="h-16 flex items-center justify-center mb-4">
              <Icon name="mdi:recycle" class="w-12 h-12 text-rose-gold" />
            </div>
            <h3 class="text-xl font-display mb-2">Sustainability</h3>
            <p class="text-gray-700">
              We strive to minimize our environmental impact through sustainable practices and packaging.
            </p>
          </div>
          
          <div class="bg-white rounded-lg shadow-md p-6 text-center">
            <div class="h-16 flex items-center justify-center mb-4">
              <Icon name="mdi:quality-high" class="w-12 h-12 text-rose-gold" />
            </div>
            <h3 class="text-xl font-display mb-2">Quality</h3>
            <p class="text-gray-700">
              We never compromise on quality, ensuring each piece meets our exacting standards.
            </p>
          </div>
        </div>
      </section>
      
      <!-- Team Section -->
      <section>
        <h2 class="text-3xl font-display mb-6">Meet Our Team</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="h-64 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20 relative">
              <div class="absolute inset-0 flex items-center justify-center">
                <Icon name="mdi:account" class="w-24 h-24 text-gray-700" />
              </div>
            </div>
            <div class="p-6 text-center">
              <h3 class="text-xl font-display mb-1">Priya Sharma</h3>
              <p class="text-gray-600 mb-3">Founder & Creative Director</p>
              <p class="text-gray-700">
                With over 15 years of experience in jewelry design, Priya brings her passion for traditional craftsmanship to every collection.
              </p>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="h-64 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20 relative">
              <div class="absolute inset-0 flex items-center justify-center">
                <Icon name="mdi:account" class="w-24 h-24 text-gray-700" />
              </div>
            </div>
            <div class="p-6 text-center">
              <h3 class="text-xl font-display mb-1">Rajesh Patel</h3>
              <p class="text-gray-600 mb-3">Head of Production</p>
              <p class="text-gray-700">
                Rajesh oversees our workshop of skilled artisans, ensuring each piece meets our quality standards.
              </p>
            </div>
          </div>
          
          <div class="bg-white rounded-lg shadow-md overflow-hidden">
            <div class="h-64 bg-gradient-to-r from-rose-gold/20 to-matte-gold/20 relative">
              <div class="absolute inset-0 flex items-center justify-center">
                <Icon name="mdi:account" class="w-24 h-24 text-gray-700" />
              </div>
            </div>
            <div class="p-6 text-center">
              <h3 class="text-xl font-display mb-1">Ananya Desai</h3>
              <p class="text-gray-600 mb-3">Customer Experience Manager</p>
              <p class="text-gray-700">
                Ananya ensures that every customer has a seamless and delightful experience with Nakhrali Fashion.
              </p>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  title: 'About Us - Nakhrali Fashion',
  description: 'Learn about our story, craftsmanship, values, and the team behind Nakhrali Fashion'
});
</script>