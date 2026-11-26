<script setup>
import SiteCover from './SiteCover.vue'
import AboutUs from './modules/AboutUs.vue'
import ServicesModule from './modules/ServicesModule.vue'
import OurLocationsInfo from './modules/OurLocationsInfo.vue'
import MainReviewModule from './modules/MainReviewModule.vue'
</script>

<template>
  <SiteCover />

  <section class="content">
    <AboutUs />
    <ServicesModule />
    <OurLocationsInfo />
    <MainReviewModule />
  </section>
</template>