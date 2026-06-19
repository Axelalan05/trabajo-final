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

  // Actions
  function setTokens(tokens: AuthTokens) {
    accessToken.value = tokens.access
    refreshToken.value = tokens.refresh
    localStorage.setItem('access', tokens.access)
    localStorage.setItem('refresh', tokens.refresh)
  }

  async function login(username: string, password: string) {
    const { data } = await api.post<AuthTokens>('/auth/login/', { username, password })
    setTokens(data)
  }

  async function register(username: string, email: string, password: string, password_confirm: string) {
    await api.post('/auth/register/', { username, email, password, password_confirm })
  }

  async function logout() {
    try {
      await api.post('/auth/logout/', { refresh: refreshToken.value })
    } finally {
      accessToken.value = null
      refreshToken.value = null
      user.value = null
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
    }
  }

  return { accessToken, refreshToken, user, isAuthenticated, setTokens, login, register, logout }
})