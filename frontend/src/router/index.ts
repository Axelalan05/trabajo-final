import { useAuthStore } from '@/stores/auth'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
      meta: { title: 'Inicio' },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { title: 'Iniciar sesión' },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { title: 'Registrarme' },
    },
    {
      path: '/perfil',
      name: 'perfil',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true, title: 'Mi perfil' },
    },
    {
      path: '/mis-juegos',
      name: 'mis-juegos',
      component: () => import('@/views/MisJuegosView.vue'),
      meta: { requiresAuth: true, title: 'Mi colección' },
    },
    {
      path: '/explorar',
      name: 'explorar',
      component: () => import('@/views/ExplorarView.vue'),
      meta: { title: 'Explorar' },
    },
    {
      path: '/juegos/:id',
      name: 'juego-detalle',
      component: () => import('@/views/JuegoDetalleView.vue'),
      meta: { title: 'Detalle del juego' },
    },
    {
      path: '/panel/juegos',
      name: 'admin-juegos',
      component: () => import('@/views/AdminJuegosView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, title: 'Administrar catálogo' },
    },
    {
      path: '/usuarios/:username',
      name: 'perfil-publico',
      component: () => import('@/views/PerfilPublicoView.vue'),
      meta: { title: 'Perfil' },
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('@/views/ForgotPasswordView.vue'),
      meta: { title: 'Recuperar contraseña' },
    },
    {
      path: '/reset-password/:uid/:token',
      name: 'reset-password',
      component: () => import('@/views/ResetPasswordView.vue'),
      meta: { title: 'Restablecer contraseña' },
    },
    {
      path: '/verify-email/:uid/:token',
      name: 'verify-email',
      component: () => import('@/views/VerifyEmailView.vue'),
      meta: { title: 'Verificar email' },
    },
    {
      path: '/panel/usuarios',
      name: 'admin-usuarios',
      component: () => import('@/views/AdminUsuariosView.vue'),
      meta: { requiresAuth: true, requiresAdmin: true, title: 'Administrar usuarios' },
    },
  ],
})

router.beforeEach(async (to) => {
  const authStore = useAuthStore()

  if (authStore.isAuthenticated && !authStore.user) {
    try {
      await authStore.fetchUser()
    } catch {
    }
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return { name: 'login' }
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return { name: 'home' }
  }
})

router.afterEach((to) => {
  const base = 'GameVault'
  document.title = to.meta.title ? `${base} - ${to.meta.title}` : base
})

export default router