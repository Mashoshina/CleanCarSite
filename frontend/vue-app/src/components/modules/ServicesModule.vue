<script setup>
import { computed, onMounted, ref } from 'vue'

const services = ref([])
const isLoading = ref(true)
const error = ref('')

const selfService = computed(() =>
  services.value.filter((service) => service.service_type === 'self_service'),
)

const staffService = computed(() =>
  services.value.filter((service) => service.service_type === 'staff_service'),
)

function vehicleLabel(vehicleType) {
  const labels = {
    pass: 'легк.',
    truck: 'груз.',
  }

  return labels[vehicleType] ?? ''
}

function formatPrice(price) {
  const value = Number(price)

  if (!Number.isFinite(value)) {
    return `${price} ₽`
  }

  return `${new Intl.NumberFormat('ru-RU', {
    maximumFractionDigits: 2,
  }).format(value)} ₽`
}

onMounted(async () => {
  try {
    const response = await fetch('/api/services/')

    if (!response.ok) {
      throw new Error('Не удалось загрузить список услуг.')
    }

    services.value = await response.json()
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
})
</script>

<template>
  <section class="content-block-vertical">
    <span class="header" style="color: var(--burgundi)">Услуги</span>

    <p v-if="isLoading" class="basic">Загружаем услуги…</p>
    <p v-else-if="error" class="basic" role="alert">{{ error }}</p>

    <div v-else class="content-block-horizontal"  id="services">
      <section class="content-block-vertical">
        <span class="aheader" style="color: var(--charcoal)">
          Мойка самообслуживания
        </span>

        <div
          v-for="service in selfService"
          :key="service.id"
          class="table-string"
        >
          <span class="basic" style="color: var(--charcoal)">
            {{ service.name }}
            <template v-if="vehicleLabel(service.vehicle_type)">
              ({{ vehicleLabel(service.vehicle_type) }})
            </template>
          </span>
          <span class="basic" style="color: var(--charcoal)">
            {{ formatPrice(service.price) }}
          </span>
        </div>

        <p v-if="selfService.length === 0" class="basic">
          Услуги пока не добавлены.
        </p>
      </section>

      <section class="content-block-vertical">
        <span class="aheader" style="color: var(--charcoal)">
          Обслуживание персоналом
        </span>

        <div
          v-for="service in staffService"
          :key="service.id"
          class="table-string"
        >
          <span class="basic" style="color: var(--charcoal)">
            {{ service.name }}
            <template v-if="vehicleLabel(service.vehicle_type)">
              ({{ vehicleLabel(service.vehicle_type) }})
            </template>
          </span>
          <span class="basic" style="color: var(--charcoal)">
            {{ formatPrice(service.price) }}
          </span>
        </div>

        <p v-if="staffService.length === 0" class="basic">
          Услуги пока не добавлены.
        </p>
      </section>
    </div>
  </section>
</template>