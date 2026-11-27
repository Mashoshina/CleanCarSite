<script setup>
import { ref } from 'vue'

const emit = defineEmits(['close', 'created'])

const name = ref('')
const rating = ref(0)
const comment = ref('')
const submitted = ref(false)
const isSubmitting = ref(false)
const errors = ref({})
const requestError = ref('')
const successMessage = ref('')

function chooseRating(value) {
  rating.value = value
  errors.value.rating = ''
}

async function submitReview() {
  submitted.value = true
  errors.value = {}
  requestError.value = ''
  successMessage.value = ''

  if (!name.value.trim()) {
    errors.value.name = 'Заполните это поле'
  }

  if (!rating.value) {
    errors.value.rating = 'Заполните это поле'
  }

  if (Object.keys(errors.value).length > 0) return

  isSubmitting.value = true

  try {
    const response = await fetch('/api/reviews/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name.value,
        rating: rating.value,
        comment: comment.value,
      }),
    })

    const result = await response.json().catch(() => ({}))

    if (!response.ok) {
      const firstError = Object.values(result).flat()[0]
      throw new Error(
        typeof firstError === 'string'
          ? firstError
          : 'Не удалось отправить отзыв.',
      )
    }

    emit('created', result)
    successMessage.value = 'Спасибо за Ваш отзыв! :)'
    name.value = ''
    rating.value = 0
    comment.value = ''
    submitted.value = false
  } catch (error) {
    requestError.value =
      error instanceof Error
        ? error.message
        : 'Не удалось связаться с сервером.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div
    class="review-form-backdrop"
    @click.self="emit('close')"
  >
    <form
      class="overlay-form"
      role="dialog"
      aria-modal="true"
      @submit.prevent="submitReview"
    >
      <div class="table-string">
        <span class="header" style="color: var(--burgundi)">
          Оставить отзыв
        </span>

        <button
          class="text-button"
          type="button"
          aria-label="Закрыть форму"
          @click="emit('close')"
        >
          <svg
            aria-hidden="true"
            viewBox="0 0 24 24"
            width="24"
            height="24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            stroke-linecap="round"
          >
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      <span class="basic">
        * — обязательные поля
      </span>

      <div class="content-block-vertical">
        <span class="aheader" style="color: var(--charocal)">Ваше имя*:</span>
        <input
          v-model="name"
          class="review-form__input basic"
          type="text"
          autocomplete="name"
          maxlength="150"
          required
          @input="errors.name = ''"
        />
        <span v-if="errors.name" class="basic" style="color: var(--burgundi)" role="alert">
          {{ errors.name }}
        </span>
    </div>

      <div class="content-block-vertical">
        <span class="aheader" style="color: var(--charocal)">Поставьте Вашу оценку*:</span>

        <div class="content-block-horizontal" role="group" aria-label="Оценка от 1 до 5">
          <button
            v-for="star in 5"
            :key="star"
            class="review-form__star-button"
            type="button"
            :aria-label="`${star} из 5`"
            :aria-pressed="rating === star"
            @click="chooseRating(star)"
          >
            <svg
              class="review-form__star"
              :class="{ 'review-form__star--filled': star <= rating }"
              viewBox="0 0 24 24"
              aria-hidden="true"
            >
              <path
                d="m12 2.5 2.94 5.96 6.58.96-4.76 4.64 1.12 6.55L12 17.52l-5.88 3.09 1.12-6.55L2.48 9.42l6.58-.96L12 2.5Z"
              />
            </svg>
          </button>
        </div>

        <span v-if="errors.rating" class="basic" style="color: var(--burgundi)" role="alert">
          {{ errors.rating }}
        </span>
    </div>

      <label class="content-block-vertical">
        <span class="aheader">Оставьте комментарий:</span>
        <textarea
          v-model="comment"
          class="review-form__input review-form__textarea basic"
          rows="5"
        />
      </label>

      <p v-if="requestError" class="basic" style="color: var(--burgundi);">
        {{ requestError }}
      </p>

      <span
        v-if="successMessage"
        class="basic"
        role="status"
        aria-live="polite"
      >
        {{ successMessage }}
      </span>

      <button
        class="bright-button"
        type="submit"
        :disabled="isSubmitting"
      >
        <span class="basic" style="color: white">
          {{ isSubmitting ? 'Отправляем…' : 'Отправить отзыв' }}
        </span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.review-form-backdrop {
  position: fixed;
  z-index: 1100;
  inset: 0;
  display: grid;
  place-items: center;
  overflow-y: auto;
  padding: 16px;
  background: rgb(0 0 0 / 45%);
}

.review-form__required-note {
  margin: 0;
  color: var(--charcoal);
}

.review-form__field {
  width: 100%;
}

.review-form__input {
  width: 100%;
  min-height: 42px;
  padding: 8px 12px;
  border: 1px solid var(--charcoal);
  border-radius: 6px;
  background: #fff;
  color: var(--charcoal);
}

.review-form__textarea {
  min-height: 120px;
  resize: vertical;
}

.review-form__rating {
  margin: 0;
  padding: 0;
  border: 0;
}

.review-form__rating legend {
  padding: 0;
  color: var(--charcoal);
}

.review-form__stars {
  display: flex;
  gap: 4px;
}

.review-form__star-button {
  display: inline-flex;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
}

.review-form__star-button:focus-visible {
  outline: 2px solid var(--charcoal);
  outline-offset: 3px;
}

.review-form__star {
  width: 32px;
  height: 32px;
  fill: transparent;
  stroke: var(--charcoal);
  stroke-width: 2px;
  stroke-linejoin: round;
}

.review-form__star--filled {
  fill: var(--burgundi);
  stroke: var(--burgundi);
}

.review-form__error {
  color: var(--burgundi);
}

.review-form__success {
  margin: 0;
  color: var(--burgundi);
}

@media (max-width: 767px) {
  .review-form-backdrop {
    place-items: start center;
    padding: 8px;
  }

  .review-form {
    width: 100%;
    max-height: calc(100dvh - 16px);
  }
}
</style>