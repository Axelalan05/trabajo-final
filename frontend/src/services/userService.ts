import type { ApiResponse, Profile } from '@/types'
import api from './api'

export const userService = {
  async getProfile(): Promise<ApiResponse<Profile>> {
    const { data } = await api.get<ApiResponse<Profile>>('/auth/profile/')
    return data
  },

  async updateProfile(payload: { bio?: string; avatar?: File }): Promise<ApiResponse<Profile>> {
    const formData = new FormData()
    if (payload.bio !== undefined) formData.append('bio', payload.bio)
    if (payload.avatar) formData.append('avatar', payload.avatar)

    const { data } = await api.patch<ApiResponse<Profile>>('/auth/profile/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return data
  },

  async getProfilePublico(username: string): Promise<ApiResponse<Profile>> {
    const { data } = await api.get<ApiResponse<Profile>>(`/auth/users/${username}/`)
    return data
  },
}