import type { ApiResponse, Profile } from '@/types'
import api from './api'

export interface AdminUser {
  id: number
  username: string
  email: string
  date_joined: string
  is_staff: boolean
  is_active: boolean
  juegos_nombres: string[]
}

export interface UserJuegoInfo {
  juego_id: number
  juego_nombre: string
  juego_imagen: string | null
  estado: string
  puntaje: number | null
  resenia: string
}

export interface AdminUserDetail extends AdminUser {
  juegos: UserJuegoInfo[]
}

export interface PaginatedUsers {
  users: AdminUser[]
  total: number
  page: number
  total_pages: number
}

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

  // Admin
  async listUsers(search: string = '', page: number = 1): Promise<PaginatedUsers> {
    const params: Record<string, string | number> = { page }
    if (search) params.search = search
    const response = await api.get('/auth/admin/users/', { params })
    return response.data.data
  },

  async getUserDetail(id: number): Promise<ApiResponse<AdminUserDetail>> {
    const { data } = await api.get<ApiResponse<AdminUserDetail>>(`/auth/admin/users/${id}/`)
    return data
  },

  async deleteUser(id: number): Promise<ApiResponse<{ message: string }>> {
    const { data } = await api.delete<ApiResponse<{ message: string }>>(`/auth/admin/users/${id}/delete/`)
    return data
  },
}
