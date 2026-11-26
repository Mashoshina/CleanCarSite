<script setup>
import { onMounted, ref } from 'vue'

const section = ref(null)
const error = ref('')
const isLoading = ref(true)

onMounted(async () => {
  try {
    const response = await fetch('api/content/about-us/')

    if (!response.ok) {
      throw new Error('Не удалось загрузить раздел «О нас».')
    }

    section.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <section v-if="section" class="content-block-vertical">
    <span class="header" style="color: var(--burgundi)">
      {{ section.title }}
    </span>

    <span class="aheader" style="color: var(--charcoal)">
      {{ section.subtitle }}
    </span>

    <span class="basic" style="color: var(--charcoal)">
      {{ section.description }}
    </span>

    <ul class="basic" style="color: var(--charcoal)">
      <li v-for="bullet in section.bullets" :key="bullet.id">
        {{ bullet.text }}
      </li>
    </ul>

    <div class="content-block-horizontal">
      <article
        v-for="feature in section.features"
        :key="feature.id"
        class="bage"
      >
        <span class="aheader" style="color: var(--burgundi)">
          {{ feature.title }}
        </span>
        <span class="basic" style="color: var(--charcoal)">
          {{ feature.description }}
        </span>
      </article>
    </div>
  </section>

  <span v-else-if="isLoading" class="basic">Загружаем раздел…</span>
  <span v-else-if="error" class="basic" role="alert">{{ error }}</span>
</template>