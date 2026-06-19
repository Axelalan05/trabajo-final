import type { ApiResponse, Juego } from '@/types'
import api from './api'

export interface JuegoFiltros {
  genero?: string
  plataforma?: string
  estado?: string
  ordering?: string
}

export const juegoService = {
  async listMios(): Promise<ApiResponse<Juego[]>> {
    const { data } = await api.get<ApiResponse<Juego[]>>('/juegos/')
    return data
  },

  async listPublico(filtros?: JuegoFiltros): Promise<ApiResponse<Juego[]>> {
    const { data } = await api.get<ApiResponse<Juego[]>>('/juegos/publico/', {
      params: filtros,
    })
    return data
  },

  async get(id: number): Promise<ApiResponse<Juego>> {
    const { data } = await api.get<ApiResponse<Juego>>(`/juegos/${id}/`)
    return data
  },

  async create(juego: Partial<Juego>): Promise<ApiResponse<Juego>> {
    const { data } = await api.post<ApiResponse<Juego>>('/juegos/', juego)
    return data
  },

  async update(id: number, juego: Partial<Juego>): Promise<ApiResponse<Juego>> {
    const { data } = await api.patch<ApiResponse<Juego>>(`/juegos/${id}/`, juego)
    return data
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/juegos/${id}/`)
  },

  async toggleFavorito(id: number): Promise<ApiResponse<null>> {
    const { data } = await api.post<ApiResponse<null>>(`/juegos/${id}/favorito/`)
    return data
  },

  async estadisticas(): Promise<ApiResponse<any>> {
    const { data } = await api.get<ApiResponse<any>>('/juegos/estadisticas/')
    return data
  },
}