import { createRouter, createWebHistory } from 'vue-router'
import calculator from '../components/calculator.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
      {
      path: '/',
      name: 'calculator',
      component: calculator
    },
  ]
})

export default router