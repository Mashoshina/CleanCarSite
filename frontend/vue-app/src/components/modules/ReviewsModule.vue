<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'

const reviews = ref([])
const isLoading = ref(true)
const error = ref('')

function isValidReview(review) {
  return (
    review &&
    typeof review.name === 'string' &&
    review.name.trim().length > 0 &&
    Number.isInteger(review.rating) &&
    review.rating >= 1 &&
    review.rating <= 5
  )
}

async function loadReviews() {
  isLoading.value = true
  error.value = ''

  try {
    const response = await fetch('/api/reviews/')

    if (!response.ok) {
      throw new Error('Не удалось загрузить отзывы.')
    }

    const data = await response.json()

    if (!Array.isArray(data) || !data.every(isValidReview)) {
      throw new Error('С отзывом что-то не так')
    }

    reviews.value = data
  } catch (err) {
    error.value =
      err instanceof Error ? err.message : 'Не удалось загрузить отзывы.'
  } finally {
    isLoading.value = false
  }
}

onMounted(loadReviews)
</script>

<template>
  <section class="content-block-vertical">
    <span class="header" style="color: var(--burgundi)">Отзывы</span>

    <span v-if="isLoading" class="basic" aria-live="polite">
      Загружаем отзывы…
    </span>

    <p v-else-if="error" class="basic" role="alert">
      {{ error }}
    </p>

    <p v-else-if="reviews.length === 0" class="basic">
      Отзывов пока нет.
    </p>

    <div v-else class="content-block-horizontal">
      <article
        v-for="review in reviews"
        :key="review.id"
        class="bage"
      >
        <span class="aheader">{{ review.name }}</span>

        <div
          class="main-reviews__stars"
          role="img"
          :aria-label="`Оценка ${review.rating} из 5`"
        >
          <svg
            v-for="star in 5"
            :key="star"
            class="main-reviews__star"
            :class="{ 'main-reviews__star--filled': star <= review.rating }"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              d="m12 2.5 2.94 5.96 6.58.96-4.76 4.64 1.12 6.55L12 17.52l-5.88 3.09 1.12-6.55L2.48 9.42l6.58-.96L12 2.5Z"
            />
          </svg>
        </div>

        <span class="basic">
          {{ review.comment?.trim() || 'Без текста' }}
        </span>
      </article>
    </div>

  </section>
</template>

<style scoped>
.main-reviews {
  width: 100%;
}

.main-reviews__title {
  margin: 0;
  color: var(--burgundi);
}

.main-reviews__list {
  display: flex;
  flex-wrap: wrap;
  align-items: stretch;
  gap: 16px;
  width: 100%;
}

.main-reviews__card {
  display: flex;
  flex: 1 1 220px;
  flex-direction: column;
  min-width: min(100%, 220px);
  padding: 16px;
  border: 2px solid var(--charcoal);
  border-radius: 16px;
  color: var(--charcoal);
}

.main-reviews__name {
  margin: 0 0 8px;
  color: var(--charcoal);
}

.main-reviews__stars {
  display: flex;
  gap: 4px;
  margin-bottom: 8px;
}

.main-reviews__star {
  width: 24px;
  height: 24px;
  fill: transparent;
  stroke: var(--charcoal);
  stroke-width: 2px;
  stroke-linejoin: round;
}

.main-reviews__star--filled {
  fill: var(--burgundi);
  stroke: var(--burgundi);
}

.main-reviews__comment {
  margin: 0;
  color: var(--charcoal);
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.main-reviews__error {
  color: var(--burgundi);
}

.main-reviews__all {
  align-self: flex-start;
}

@media (max-width: 767px) {
  .main-reviews__card {
    flex-basis: 100%;
  }
}
</style>