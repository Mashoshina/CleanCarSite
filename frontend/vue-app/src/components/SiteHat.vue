<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const isMenuOpen = ref(false)

const menuItems = [
  { label: 'Главная', to: '/' },
  { label: 'Услуги', to: '/services' },
  { label: 'Отзывы', to: '/reviews' }
]

const socialLinks = [
  {
    label: 'ВКонтакте',
    href: 'https://vk.com/',
    src: '/items/VK_icons_logo_vk_outline_28.svg',
  },
  {
    label: 'MAX',
    href: 'https://max.ru/',
    src: '/items/Логотип_MAX.svg',
  },
  {
    label: 'Telegram',
    href: 'https://t.me/',
    src: '/items/Telegram_logo_icon.svg',
  },
]

function closeMenu() {
  isMenuOpen.value = false
}
</script>

<template>
  <header class="site-hat" @keydown.esc="closeMenu">
    <div class="site-hat__bar">
      <button
        class="text-button site-hat__menu-toggle"
        type="button"
        :aria-expanded="isMenuOpen"
        aria-controls="site-hat-menu"
        :aria-label="isMenuOpen ? 'Закрыть меню' : 'Открыть меню'"
        @click="isMenuOpen = !isMenuOpen"
      >
        <!-- Feather-style menu icon -->
        <svg
          v-if="!isMenuOpen"
          aria-hidden="true"
          viewBox="0 0 24 24"
          width="24"
          height="24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
        >
          <line x1="3" y1="6" x2="21" y2="6" />
          <line x1="3" y1="12" x2="21" y2="12" />
          <line x1="3" y1="18" x2="21" y2="18" />
        </svg>

        <svg
          v-else
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

      <RouterLink class="big-header-2 site-hat__logo" to="/" @click="closeMenu">
        CleanCar
      </RouterLink>

      <nav class="site-hat__desktop-menu" aria-label="Основная навигация">
        <RouterLink
          v-for="item in menuItems"
          :key="item.label"
          class="text-button"
          :to="item.to"
          @click="closeMenu"
        >
          <span class="basic">{{ item.label }}</span>
        </RouterLink>
      </nav>

      <div class="site-hat__desktop-socials" aria-label="Социальные сети">
        <a
          v-for="social in socialLinks"
          :key="social.label"
          class="text-button site-hat__social-link"
          :href="social.href"
          :aria-label="social.label"
          target="_blank"
          rel="noopener noreferrer"
        >
          <img :src="social.src" :alt="social.label" />
        </a>
      </div>
    </div>

    <template v-if="isMenuOpen">
      <button
        class="site-hat__backdrop"
        type="button"
        aria-label="Закрыть меню"
        @click="closeMenu"
      />

      <nav
        id="site-hat-menu"
        class="site-hat__mobile-panel"
        aria-label="Основная навигация"
      >
        <div class="site-hat__mobile-menu">
          <RouterLink
            v-for="item in menuItems"
            :key="item.label"
            class="text-button"
            :to="item.to"
            @click="closeMenu"
          >
            <span class="basic">{{ item.label }}</span>
          </RouterLink>
        </div>

        <div class="site-hat__mobile-socials" aria-label="Социальные сети">
          <a
            v-for="social in socialLinks"
            :key="social.label"
            class="text-button site-hat__social-link"
            :href="social.href"
            :aria-label="social.label"
            target="_blank"
            rel="noopener noreferrer"
          >
            <img :src="social.src" :alt="social.label" />
          </a>
        </div>
      </nav>
    </template>
  </header>
</template>

<style scoped>

.site-hat {
  position: sticky;
  z-index: 20;
  top: 0;
  width: 100%;
  color: var(--charcoal);
}

.site-hat__bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  width: 100%;
  padding: 24px clamp(16px, 5.56vw, 80px);
  border-bottom: 2px solid #000;
  background: var(--alice-blue);
}

.site-hat__logo {
  flex: 0 0 auto;
  color: inherit;
  text-decoration: none;
}

.site-hat__desktop-menu,
.site-hat__desktop-socials,
.site-hat__mobile-socials {
  display: flex;
  align-items: center;
}

.site-hat__desktop-menu {
  gap: 48px;
}

.site-hat__desktop-socials,
.site-hat__mobile-socials {
  gap: 16px;
}

.site-hat__social-link img {
  display: block;
  width: 28px;
  height: 28px;
  object-fit: contain;
}

.site-hat__menu-toggle,
.site-hat__mobile-panel,
.site-hat__backdrop {
  display: none;
}


@media (max-width: 1100px) {
  .site-hat__bar {
    justify-content: flex-start;
    gap: 16px;
    padding: 16px 24px;
  }

  .site-hat__menu-toggle {
    display: inline-flex;
    flex: 0 0 auto;
  }

  .site-hat__logo {
    font-size: 36px;
  }

  .site-hat__desktop-menu,
  .site-hat__desktop-socials {
    display: none;
  }

  .site-hat__backdrop {
    position: fixed;
    z-index: 1;
    inset: 0;
    display: block;
    width: 100%;
    height: 100%;
    border: 0;
    background: rgb(0 0 0 / 45%);
  }

  .site-hat__mobile-panel {
    position: absolute;
    z-index: 2;
    top: 100%;
    left: 0;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 128px;
    width: min(320px, 100vw);
    max-height: calc(100dvh - 80px);
    overflow-y: auto;
    padding: 16px 24px;
    background: var(--alice-blue);
  }

  .site-hat__mobile-menu {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .site-hat__mobile-socials {
    display: flex;
  }
}
</style>