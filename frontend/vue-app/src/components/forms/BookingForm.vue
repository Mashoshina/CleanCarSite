<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps({
  selectedLocation: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['close', 'booked'])

const address = ref('')
const addressSuggestions = ref([])
const selectedPoint = ref(null)
const addressMessage = ref('')
const addressError = ref('')

const supportedFormats = ref([])
const selectedFormat = ref('')

const selectedDate = ref('')
const selectedTime = ref('')
const availableTimes = ref([])
const availabilityError = ref('')
const isLoadingTimes = ref(false)

const clientName = ref('')
const phoneDigits = ref('')
const phoneError = ref('')
const requiredError = ref(false)

const isSubmitting = ref(false)
const submitError = ref('')

const today = getLocalToday()
const visibleMonth = ref(startOfMonth(new Date()))
let addressSearchTimer = null
let addressSearchController = null
let availabilityController = null

const weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

const monthTitle = computed(() =>
  visibleMonth.value.toLocaleDateString('ru-RU', {
    month: 'long',
    year: 'numeric',
  }),
)

const calendarDays = computed(() => {
  const year = visibleMonth.value.getFullYear()
  const month = visibleMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const offset = (firstDay.getDay() + 6) % 7
  const daysInMonth = new Date(year, month + 1, 0).getDate()

  return [
    ...Array.from({ length: offset }, (_, index) => ({
      key: `empty-${index}`,
      empty: true,
    })),
    ...Array.from({ length: daysInMonth }, (_, index) => {
      const day = index + 1
      const value = toDateString(new Date(year, month, day))

      return {
        key: value,
        day,
        value,
        empty: false,
        disabled: value < today,
        isToday: value === today,
        isSelected: value === selectedDate.value,
      }
    }),
  ]
})

const canGoToPreviousMonth = computed(() => {
  const current = visibleMonth.value
  const currentYear = Number(today.slice(0, 4))
  const currentMonth = Number(today.slice(5, 7)) - 1

  return (
    current.getFullYear() > currentYear ||
    (current.getFullYear() === currentYear &&
      current.getMonth() > currentMonth)
  )
})

function getLocalToday() {
  return toDateString(new Date())
}

function toDateString(date) {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function startOfMonth(date) {
  return new Date(date.getFullYear(), date.getMonth(), 1)
}

function moveMonth(offset) {
  const current = visibleMonth.value
  visibleMonth.value = new Date(
    current.getFullYear(),
    current.getMonth() + offset,
    1,
  )
}

function selectDate(date) {
  if (date < today) return

  selectedDate.value = date
  selectedTime.value = ''
  loadAvailability()
}

function getLocationFormats(location) {
  if (!location) return []

  if (Array.isArray(location.available_booking_types)) {
    return location.available_booking_types
  }

  if (location.location_type === 'both') {
    return ['self_service', 'staff_service']
  }

  return location.location_type ? [location.location_type] : []
}

function setSelectedPoint(location) {
  selectedPoint.value = location
  address.value = location?.address ?? ''
  addressError.value = ''
  addressMessage.value = ''
  addressSuggestions.value = []

  supportedFormats.value = getLocationFormats(location)
  selectedFormat.value =
    supportedFormats.value.length === 1 ? supportedFormats.value[0] : ''

  selectedTime.value = ''
  availableTimes.value = []

  if (location) {
    loadAvailability()
  }
}

function onAddressInput() {
  selectedPoint.value = null
  supportedFormats.value = []
  selectedFormat.value = ''
  selectedTime.value = ''
  availableTimes.value = []
  addressError.value = ''
  addressMessage.value = ''
  requiredError.value = false

  clearTimeout(addressSearchTimer)
  addressSearchController?.abort()

  const query = address.value.trim()
  if (query.length < 2) {
    addressSuggestions.value = []
    return
  }

  addressSearchTimer = setTimeout(searchAddresses, 300)
}

async function searchAddresses() {
  const query = address.value.trim()
  if (query.length < 2) return

  addressSearchController?.abort()
  addressSearchController = new AbortController()

  try {
    const params = new URLSearchParams({ q: query })
    const response = await fetch(`/api/locations/search/?${params}`, {
      signal: addressSearchController.signal,
    })

    if (!response.ok) {
      throw new Error('Не удалось выполнить поиск адреса.')
    }

    addressSuggestions.value = await response.json()
    addressMessage.value =
      addressSuggestions.value.length === 0 ? 'Неверный ввод адреса' : ''
  } catch (error) {
    if (error.name !== 'AbortError') {
      addressSuggestions.value = []
      addressMessage.value = 'Не удалось загрузить подсказки адресов.'
    }
  }
}

async function chooseAddress(suggestion) {
  address.value = suggestion.address
  addressSuggestions.value = []
  addressMessage.value = ''
  addressError.value = ''

  try {
    const params = new URLSearchParams({
      q: suggestion.address,
      date: selectedDate.value,
    })
    const response = await fetch(`/api/locations/?${params}`)

    if (!response.ok) {
      throw new Error('Не удалось загрузить данные точки.')
    }

    const points = await response.json()
    const point = points.find((item) => item.id === suggestion.id)

    if (!point) {
      selectedPoint.value = null
      addressError.value = 'Неверный адрес'
      return
    }

    setSelectedPoint(point)
  } catch {
    selectedPoint.value = null
    addressError.value = 'Не удалось загрузить выбранную точку.'
  }
}

async function loadAvailability() {
  if (!selectedPoint.value || !selectedDate.value) return

  availabilityController?.abort()
  availabilityController = new AbortController()

  isLoadingTimes.value = true
  availabilityError.value = ''
  selectedTime.value = ''

  try {
    const params = new URLSearchParams({
      q: selectedPoint.value.address,
      date: selectedDate.value,
    })
    const response = await fetch(`/api/locations/?${params}`, {
      signal: availabilityController.signal,
    })

    if (!response.ok) {
      throw new Error('Не удалось загрузить свободное время.')
    }

    const points = await response.json()
    const point = points.find((item) => item.id === selectedPoint.value.id)

    if (!point) {
      throw new Error('Выбранная точка больше недоступна.')
    }

    selectedPoint.value = point
    availableTimes.value = point.available_times ?? []
    supportedFormats.value = getLocationFormats(point)

    if (
      supportedFormats.value.length === 1 &&
      !selectedFormat.value
    ) {
      selectedFormat.value = supportedFormats.value[0]
    }
  } catch (error) {
    if (error.name !== 'AbortError') {
      availabilityError.value =
        error instanceof Error
          ? error.message
          : 'Не удалось загрузить свободное время.'
      availableTimes.value = []
    }
  } finally {
    if (!availabilityController.signal.aborted) {
      isLoadingTimes.value = false
    }
  }
}

function chooseFormat(format) {
  if (supportedFormats.value.length > 1) {
    selectedFormat.value = format
  }
}

function validatePhone() {
  phoneDigits.value = phoneDigits.value.replace(/\D/g, '').slice(0, 10)
}

function validateForm() {
  requiredError.value = false
  addressError.value = ''
  phoneError.value = ''
  submitError.value = ''

  let isValid = true

  if (!selectedPoint.value) {
    addressError.value = 'Неверный адрес'
    isValid = false
  }

  if (!clientName.value.trim() || !selectedFormat.value ||
      !selectedDate.value || !selectedTime.value || !phoneDigits.value) {
    requiredError.value = true
    isValid = false
  }

  if (phoneDigits.value.length !== 10) {
    phoneError.value = 'Неверный формат номера телефона'
    isValid = false
  }

  return isValid
}

async function submitBooking() {
  if (!validateForm()) return

  isSubmitting.value = true
  submitError.value = ''

  try {
    const response = await fetch('/api/bookings/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        location: selectedPoint.value.id,
        client_name: clientName.value.trim(),
        client_phone: `+7${phoneDigits.value}`,
        booking_date: selectedDate.value,
        booking_time: selectedTime.value,
        booking_type: selectedFormat.value,
      }),
    })

    const result = await response.json().catch(() => ({}))

    if (!response.ok) {
      if (response.status === 409 || result.booking_time) {
        availabilityError.value =
          result.booking_time?.[0] ??
          'Это время уже занято. Выберите другое.'
        await loadAvailability()
      } else {
        submitError.value =
          result.detail ??
          'Не удалось создать запись. Проверьте введённые данные.'
      }
      return
    }

    emit('booked', result)
    emit('close')
  } catch {
    submitError.value = 'Не удалось связаться с сервером.'
  } finally {
    isSubmitting.value = false
  }
}

function onEscape(event) {
  if (event.key === 'Escape') {
    emit('close')
  }
}

watch(
  () => props.selectedLocation,
  (location) => {
    if (location) {
      setSelectedPoint(location)
    }
  },
  { immediate: true },
)

watch(selectedDate, () => {
  if (selectedPoint.value) {
    loadAvailability()
  }
})

onMounted(() => {
  selectedDate.value = today
  visibleMonth.value = startOfMonth(new Date())
  window.addEventListener('keydown', onEscape)
})

onBeforeUnmount(() => {
  clearTimeout(addressSearchTimer)
  addressSearchController?.abort()
  availabilityController?.abort()
  window.removeEventListener('keydown', onEscape)
})
</script>

<template>
  <div class="booking-form-backdrop" @click.self="emit('close')">
    <form class="overlay-form booking-form" @submit.prevent="submitBooking">
      <div class="table-string booking-form__heading">
        <h2 class="header" style="color: var(--burgundi)">
          Запись в онлайн-очередь
        </h2>

        <button
          class="text-button booking-form__close"
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

      <p class="basic" :style="{ color: requiredError ? 'var(--burgundi)' : 'var(--charcoal)' }">
        * — обязательные поля
      </p>

      <section class="content-block-vertical booking-form__field">
        <label class="aheader" for="booking-address">
          Адрес*
        </label>

        <input
          id="booking-address"
          v-model="address"
          class="form-input basic"
          type="search"
          autocomplete="street-address"
          placeholder="Начните вводить адрес точки"
          aria-autocomplete="list"
          @input="onAddressInput"
        />

        <p v-if="addressError" class="basic booking-form__error" role="alert">
          {{ addressError }}
        </p>

        <ul
          v-if="addressSuggestions.length || addressMessage"
          class="booking-form__suggestions"
          role="listbox"
        >
          <li
            v-for="suggestion in addressSuggestions"
            :key="suggestion.id"
            class="booking-form__suggestion"
            role="option"
            @click="chooseAddress(suggestion)"
          >
            {{ suggestion.address }}
          </li>
          <li
            v-if="addressMessage"
            class="booking-form__suggestion booking-form__suggestion--message"
          >
            {{ addressMessage }}
          </li>
        </ul>
      </section>

      <section class="content-block-vertical booking-form__field">
        <span class="aheader">Формат*</span>

        <div class="content-block-horizontal booking-form__choices">
          <button
            v-for="format in supportedFormats"
            :key="format"
            class="general-button"
            :class="{ 'is-selected': selectedFormat === format }"
            :aria-pressed="selectedFormat === format"
            type="button"
            @click="chooseFormat(format)"
          >
            <span class="basic">
              {{
                format === 'self_service'
                  ? 'Мойка самообслуживания'
                  : 'Обслуживание персоналом'
              }}
            </span>
          </button>

          <span v-if="!selectedPoint" class="basic">
            Сначала выберите адрес точки.
          </span>
        </div>
      </section>

      <section class="content-block-vertical booking-form__field">
        <span class="aheader">Дата*</span>

        <div class="booking-calendar">
          <div class="booking-calendar__header">
            <button
              class="text-button"
              type="button"
              aria-label="Предыдущий месяц"
              :disabled="!canGoToPreviousMonth"
              @click="moveMonth(-1)"
            >
              ‹
            </button>
            <span class="basic">{{ monthTitle }}</span>
            <button
              class="text-button"
              type="button"
              aria-label="Следующий месяц"
              @click="moveMonth(1)"
            >
              ›
            </button>
          </div>

          <div class="booking-calendar__grid">
            <span
              v-for="weekday in weekdays"
              :key="weekday"
              class="basic booking-calendar__weekday"
            >
              {{ weekday }}
            </span>

            <span
              v-for="day in calendarDays"
              :key="day.key"
              class="booking-calendar__day-cell"
            >
              <span v-if="day.empty" />
              <button
                v-else
                class="general-button booking-calendar__day"
                :class="{
                  'is-selected': day.isSelected,
                  'booking-calendar__day--today': day.isToday,
                }"
                :disabled="day.disabled"
                :aria-pressed="day.isSelected"
                type="button"
                @click="selectDate(day.value)"
              >
                <span class="basic">{{ day.day }}</span>
              </button>
            </span>
          </div>
        </div>
      </section>

      <section class="content-block-vertical booking-form__field">
        <span class="aheader">Доступное время*</span>

        <p v-if="isLoadingTimes" class="basic">Загружаем время…</p>
        <p v-else-if="availabilityError" class="basic booking-form__error" role="alert">
          {{ availabilityError }}
        </p>
        <p v-else-if="selectedPoint && availableTimes.length === 0" class="basic">
          На выбранную дату свободного времени нет.
        </p>

        <div v-if="availableTimes.length" class="booking-form__times">
          <button
            v-for="time in availableTimes"
            :key="time"
            class="general-button booking-form__time"
            :class="{ 'is-selected': selectedTime === time }"
            :aria-pressed="selectedTime === time"
            type="button"
            @click="selectedTime = time"
          >
            <span class="basic">{{ time }}</span>
          </button>
        </div>
      </section>

      <section class="content-block-vertical booking-form__field">
        <label class="aheader" for="booking-name">Имя*</label>
        <input
          id="booking-name"
          v-model="clientName"
          class="form-input basic"
          type="text"
          autocomplete="name"
          maxlength="150"
          required
        />
      </section>

      <section class="content-block-vertical booking-form__field">
        <label class="aheader" for="booking-phone">Телефон*</label>

        <div class="booking-form__phone">
          <span class="basic">+7</span>
          <input
            id="booking-phone"
            v-model="phoneDigits"
            class="form-input basic"
            type="tel"
            inputmode="numeric"
            autocomplete="tel-national"
            maxlength="10"
            placeholder="___ ___ __ __"
            required
            @input="validatePhone"
          />
        </div>

        <p v-if="phoneError" class="basic booking-form__error" role="alert">
          {{ phoneError }}
        </p>
      </section>

      <p v-if="submitError" class="basic booking-form__error" role="alert">
        {{ submitError }}
      </p>

      <button
        class="bright-button"
        type="submit"
        :disabled="isSubmitting"
      >
        <span class="basic">
          {{ isSubmitting ? 'Отправляем…' : 'Записаться' }}
        </span>
      </button>
    </form>
  </div>
</template>

<style scoped>
.booking-form-backdrop {
  position: fixed;
  z-index: 1000;
  inset: 0;
  display: grid;
  place-items: center;
  overflow-y: auto;
  padding: 16px;
  background: rgb(0 0 0 / 45%);
}

.booking-form {
  width: min(700px, 100%);
  max-height: calc(100dvh - 32px);
  overflow-y: auto;
}

.booking-form__heading {
  align-items: center;
}

.booking-form__close {
  flex: 0 0 auto;
}

.booking-form__field {
  width: 100%;
}

.form-input {
  width: 100%;
  min-height: 42px;
  padding: 8px 12px;
  border: 1px solid var(--charcoal);
  border-radius: 6px;
  background: #fff;
  color: var(--charcoal);
}

.booking-form__error {
  color: var(--burgundi);
}

.booking-form__suggestions {
  width: 100%;
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid var(--charcoal);
  background: #fff;
}

.booking-form__suggestion {
  padding: 8px 12px;
  cursor: pointer;
}

.booking-form__suggestion:hover {
  background: var(--alice-blue);
}

.booking-form__suggestion--message {
  color: var(--burgundi);
  cursor: default;
}

.booking-form__choices {
  align-items: stretch;
}

.general-button.is-selected {
  background: var(--burgundi);
  border-color: var(--burgundi);
  color: #fff;
}

.booking-calendar {
  width: min(360px, 100%);
}

.booking-calendar__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px;
}

.booking-calendar__grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 4px;
}

.booking-calendar__weekday {
  text-align: center;
}

.booking-calendar__day-cell {
  display: grid;
  min-width: 0;
}

.booking-calendar__day {
  width: 100%;
  min-width: 0;
  padding: 6px 2px;
}

.booking-calendar__day--today:not(.is-selected) {
  border-color: var(--burgundi);
}

.booking-calendar__times {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.booking-form__times {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  width: 100%;
}

.booking-form__time {
  flex: 1 1 80px;
  min-width: 80px;
}

.booking-form__phone {
  display: flex;
  align-items: center;
  gap: 8px;
}

.booking-form__phone .form-input {
  flex: 1;
}

@media (max-width: 767px) {
  .booking-form-backdrop {
    place-items: start center;
    padding: 8px;
  }

  .booking-form {
    max-height: calc(100dvh - 16px);
  }

  .booking-form__time {
    flex-basis: 70px;
    min-width: 70px;
  }
}
</style>