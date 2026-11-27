import { createRouter, createWebHistory } from 'vue-router'
import MainPage from '../components/MainPage.vue'
import ServicesPage from '../components/ServicesPage.vue'
import ReviewsModule from '../components/ReviewsPage.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MainPage,
    },
    {
      path: '/services',
      name: 'services',
      component: ServicesPage,
    },
    {
      path: '/reviews',
      name: 'reviews',
      component: ReviewsModule,
    },
  ],
})

export default router