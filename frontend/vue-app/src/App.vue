<script setup>
import { onMounted, ref } from 'vue'
import SiteHat from './components/SiteHat.vue'

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
  <SiteHat />
  <main>
    <h1>Доступные точки CleanCar</h1>

    <p v-if="isLoading">Загружаем адреса…</p>
    <p v-else-if="error">{{ error }}</p>
    <p v-else-if="locations.length === 0">Активных точек пока нет.</p>

    <ul v-else>
      <li v-for="location in locations" :key="location.id">
        {{ location.address }}
      </li>
    </ul>
  </main>
</template>
