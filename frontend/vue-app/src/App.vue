<script setup>
import { onMounted, ref } from 'vue'
import { RouterView } from 'vue-router'
import SiteHat from './components/SiteHat.vue'
import SiteFooter from './components/SiteFooter.vue'


const locations = ref([])
const isLoading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await fetch('/locations/api/')

    if (!response.ok) {
      throw new Error('Не удалось загрузить список точек')
    }

    locations.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <div class="page">
    <SiteHat />

    <main class="page__content">
      <RouterView />
    </main>

    <SiteFooter />
  </div>
</template>
