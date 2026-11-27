<script setup>
import { ref } from 'vue'
import ReviewsModule from './modules/ReviewsModule.vue'
import ReviewForm from './forms/ReviewForm.vue'

const isReviewFormOpen = ref(false)
const reviewsKey = ref(0)

function handleReviewSubmitted() {
  // Пересоздание ReviewsModule запускает повторную загрузку списка.
  reviewsKey.value += 1
}
</script>

<template>
  <section class="content">
    <ReviewsModule :key="reviewsKey"/>
    
    <button
      class="bright-button"
      type="button"
      @click="isReviewFormOpen = true"
    >
      <span class="basic">Оставить отзыв</span>
    </button>
  </section>

  <ReviewForm
    v-if="isReviewFormOpen"
    @close="isReviewFormOpen = false"
    @created="handleReviewSubmitted"
  />
</template>