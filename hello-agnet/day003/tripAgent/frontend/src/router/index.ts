import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue')
    },
    {
      path: '/result',
      name: 'result',
      component: () => import('@/views/Result.vue')
    }
  ]
})

export default router
