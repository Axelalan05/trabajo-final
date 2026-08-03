import api from '@/services/api'
import type { AuthTokens, User } from '@/types'
import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // State
  const accessToken = ref<string | null>(localStorage.getItem('access'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh'))
  const user = ref<User | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!accessToken.value)
  const isAdmin = computed(() => !!user.value?.is_staff)

  // Actions
  function setTokens(tokens: AuthTokens) {
    accessToken.value = tokens.access
    refreshToken.value = tokens.refresh
    localStorage.setItem('access', tokens.access)
    localStorage.setItem('refresh', tokens.refresh)
  }

  async function fetchUser() {
    const { data } = await api.get<{ success: boolean; data: User }>('/auth/me/')
    user.value = data.data
  }

  async function login(username: string, password: string) {
    const { data } = await api.post<AuthTokens>('/auth/login/', { username, password })
    setTokens(data)
    await fetchUser()
  }

  async function register(username: string, email: string, password: string, password_confirm: string) {
    await api.post('/auth/register/', { username, email, password, password_confirm })
  }

  async function logout() {
    try {
      await api.post('/auth/logout/', { refresh: refreshToken.value })
    } catch (error) {
      console.error('No se pudo notificar el logout al backend:', error)
    } finally {
      accessToken.value = null
      refreshToken.value = null
      user.value = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    }
  }

  return { accessToken, refreshToken, user, isAuthenticated, isAdmin, setTokens, login, register, logout, fetchUser }
})