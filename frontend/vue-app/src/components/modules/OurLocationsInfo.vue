<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'
import markerIconUrl from 'leaflet/dist/images/marker-icon.png'
import markerShadowUrl from 'leaflet/dist/images/marker-shadow.png'
import BookingForm from '../forms/BookingForm.vue'

const mapElement = ref(null)
const locations = ref([])
const selectedLocation = ref(null)
const selectedTypes = ref([])
const addressQuery = ref('')
const error = ref('')
const mapError = ref('')
const isLoading = ref(false)

let map = null
let markerLayer = null
let searchTimeout = null
let requestController = null

const markerIcon = L.icon({
  iconUrl: markerIconUrl,
  shadowUrl: markerShadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  shadowSize: [41, 41],
})

const allTypesSelected = computed(() => selectedTypes.value.length === 2)

const isBookingFormOpen = ref(false)

function reserveOnline() {
  if (!selectedLocation.value) return
  isBookingFormOpen.value = true
}

function handleBookingCreated() {
  isBookingFormOpen.value = false
  loadLocations()
}

function toggleType(type) {
  if (selectedTypes.value.includes(type)) {
    selectedTypes.value = selectedTypes.value.filter((item) => item !== type)
  } else {
    selectedTypes.value = [...selectedTypes.value, type]
  }

  loadLocations()
}

function getLocalToday() {
  const now = new Date()
  const year = now.getFullYear()
  const month = String(now.getMonth() + 1).padStart(2, '0')
  const day = String(now.getDate()).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function formatLabel(locationType) {
  const labels = {
    self_service: 'Самообслуживание',
    staff_service: 'Обслуживание персоналом',
    both: 'Самообслуживание и обслуживание персоналом',
  }

  return labels[locationType] ?? locationType
}

function scheduleAddressSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(loadLocations, 300)
}

async function loadLocations() {
  requestController?.abort()
  requestController = new AbortController()

  const currentController = requestController
  isLoading.value = true
  error.value = ''

  const params = new URLSearchParams()
  const query = addressQuery.value.trim()

  params.set('date', getLocalToday())

  if (query) {
    params.set('q', query)
  }

  if (allTypesSelected.value) {
    params.set('type', 'both')
  } else if (selectedTypes.value.length === 1) {
    params.set('type', selectedTypes.value[0])
  }

  const url = `/api/locations/?${params.toString()}`

  try {
    const response = await fetch(url, {
      signal: currentController.signal,
    })

    if (!response.ok) {
      throw new Error('Не удалось загрузить список точек.')
    }

    locations.value = await response.json()

    if (selectedLocation.value) {
      selectedLocation.value =
        locations.value.find(
          (location) => location.id === selectedLocation.value.id,
        ) ?? null
    }

    updateMarkers()
  } catch (err) {
    if (err.name !== 'AbortError') {
      error.value =
        err instanceof Error ? err.message : 'Произошла ошибка.'
      locations.value = []
      selectedLocation.value = null
      updateMarkers()
    }
  } finally {
    if (requestController === currentController) {
      isLoading.value = false
    }
  }
}

function updateMarkers() {
  if (!map || !markerLayer) return

  markerLayer.clearLayers()

  const validLocations = locations.value.filter((location) => {
    return (
      Number.isFinite(Number(location.latitude)) &&
      Number.isFinite(Number(location.longitude))
    )
  })

  validLocations.forEach((location) => {
    const marker = L.marker(
      [Number(location.latitude), Number(location.longitude)],
      { icon: markerIcon },
    )

    marker.on('click', () => {
      selectedLocation.value = location
    })

    marker.addTo(markerLayer)
  })

  if (validLocations.length === 1) {
    const location = validLocations[0]
    map.setView(
      [Number(location.latitude), Number(location.longitude)],
      14,
    )
  } else if (validLocations.length > 1) {
    const bounds = L.latLngBounds(
      validLocations.map((location) => [
        Number(location.latitude),
        Number(location.longitude),
      ]),
    )

    map.fitBounds(bounds, { padding: [24, 24], maxZoom: 14 })
  }
}

onMounted(() => {
  try {
    map = L.map(mapElement.value).setView([55.16, 61.4], 10)

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)

    markerLayer = L.layerGroup().addTo(map)

    loadLocations()

    requestAnimationFrame(() => {
      map?.invalidateSize()
    })
  } catch {
    mapError.value = 'Не удалось инициализировать карту.'
  }
})

onBeforeUnmount(() => {
  clearTimeout(searchTimeout)
  requestController?.abort()
  map?.remove()
  map = null
  markerLayer = null
})
</script>

<template>
  <section class="content-block-vertical">
    <span class="header" style="color: var(--burgundi)">Наши точки</span>

    <div class="content-block-horizontal">
      <section class="content-block-vertical">
        <span class="basic">
          Выберите на карте адрес подходящей точки и запишитесь в онлайн-очереди.
        </span>

        <label class="basic">
          Поиск по адресу
          <input
            v-model="addressQuery"
            type="search"
            placeholder="Введите адрес"
            @input="scheduleAddressSearch"
          />
        </label>

        <div class="content-block-vertical">
          <button
            class="general-button"
            :class="{ 'is-selected': selectedTypes.includes('self_service') }"
            :aria-pressed="selectedTypes.includes('self_service')"
            @click="toggleType('self_service')"
          >
            <span class="basic">Мойка самообслуживания</span>
          </button>

          <button
            class="general-button"
            :class="{ 'is-selected': selectedTypes.includes('staff_service') }"
            :aria-pressed="selectedTypes.includes('staff_service')"
            @click="toggleType('staff_service')"
          >
            <span class="basic">Обслуживание персоналом</span>
          </button>
        </div>

        <span v-if="isLoading" class="basic">Загружаем точки…</span>
        <span v-else-if="error" class="basic" role="alert">{{ error }}</span>
        <span v-else-if="locations.length === 0" class="basic">
          По выбранным параметрам активных точек нет.
        </span>

        <div v-if="locations.length" class="content-block-vertical">
          <span class="aheader" style="color: var(--burgundi)">
            Информация о выбранной точке
          </span>

          <span v-if="!selectedLocation" class="basic">Точка не выбрана.</span>

          <template v-else>
            <span class="basic">Адрес: {{ selectedLocation.address }}</span>
            <span class="basic">Формат: {{ formatLabel(selectedLocation.location_type) }}</span>
            <span class="basic">Номер телефона: {{ selectedLocation.phone }}</span>
            <span class="basic">Доступное время сегодня:</span>

            <div class="content-block-horizontal locations-times">
              <span
                v-for="time in selectedLocation.available_times"
                :key="time"
                class="small-bage basic"
              >
                {{ time }}
              </span>

              <span
                v-if="selectedLocation.available_times.length === 0"
                class="basic"
              >
                Свободного времени сегодня нет.
              </span>
            </div>
          </template>

          <button
            class="bright-button"
            type="button"
            :disabled="!selectedLocation"
            @click="reserveOnline"
          >
            <span class="basic">Занять онлайн очередь</span>
          </button>
        </div>
      </section>
      <BookingForm
        v-if="isBookingFormOpen"
        :selected-location="selectedLocation"
        @close="isBookingFormOpen = false"
        @booked="handleBookingCreated"
      />
      <p v-if="mapError" class="basic" role="alert">{{ mapError }}</p>

<div
  ref="mapElement"
  class="locations-map"
  role="region"
  aria-label="Карта доступных точек CleanCar"
/>
    </div>
  </section>
</template>

<style scoped>
.locations-map {
  flex: 2 1 600px;
  width: 100%;
  max-width: 1300px;
  height: auto;
  min-height: 0;
  aspect-ratio: 16 / 9;
  align-self: flex-start;
  z-index: 19;
}

.locations-times {
  align-items: stretch;
}


.small-bage {
  display: flex;
  flex: 1 1 80px;
  align-items: center;
  justify-content: center;
  min-width: 80px;
  padding: 8px 16px;
  border: 2px solid var(--charcoal);
  border-radius: 16px;
  color: var(--charcoal);
  text-align: center;
}

.general-button.is-selected {
  background-color: var(--burgundi);
  color: white;
}

.general-button.is-selected:hover {
  background-color: var(--burgundi);
  border-color: var(--burgundi);
  color: white;
}

@media (max-width: 767px) {
  .locations-map {
    flex-basis: 100%;
  }

  .small-bage {
    padding: 4px 8px;
    border-radius: 8px;
  }
}
</style>