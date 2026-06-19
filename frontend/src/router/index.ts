import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/mis-juegos',
      name: 'mis-juegos',
      component: () => import('@/views/MisJuegosView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/explorar',
      name: 'explorar',
      component: () => import('@/views/ExplorarView.vue'),
    },
    {
      path: '/usuarios/:username',
      name: 'perfil-publico',
      component: () => import('@/views/PerfilPublicoView.vue'),
    },
  ],
})

router.beforeEach((to) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }
})

export default router