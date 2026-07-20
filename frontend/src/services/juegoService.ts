import type { ApiResponse, Juego, RawgDetalle, RawgResultado } from '@/types'
import api from './api'

export interface JuegoFiltros {
  nombre?: string
  genero?: string
  plataforma?: string
  ordering?: string
}

export const juegoService = {
  async listCatalogo(filtros?: JuegoFiltros): Promise<ApiResponse<Juego[]>> {
    const { data } = await api.get<ApiResponse<Juego[]>>('/juegos/', {
      params: filtros,
    })
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

  // Búsqueda e integración con RAWG (solo admin)
  async rawgBuscar(query: string): Promise<ApiResponse<RawgResultado[]>> {
    const { data } = await api.get<ApiResponse<RawgResultado[]>>('/juegos/rawg/buscar/', {
      params: { q: query },
    })
    return data
  },

  async rawgDetalle(rawgId: number): Promise<ApiResponse<RawgDetalle>> {
    const { data } = await api.get<ApiResponse<RawgDetalle>>(`/juegos/rawg/${rawgId}/`)
    return data
  },
}