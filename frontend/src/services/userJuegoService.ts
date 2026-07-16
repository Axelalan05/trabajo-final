import type { ApiResponse, EstadoJuego, UserJuego } from '@/types'
import api from './api'

export interface UnirseAJuegoPayload {
  juego_id: number
  estado?: EstadoJuego
  puntaje?: number | null
  resenia?: string
}

export interface ActualizarUserJuegoPayload {
  estado?: EstadoJuego
  puntaje?: number | null
  resenia?: string
}

export interface EstadisticasUsuario {
  juegos_completados: number
  promedio_puntaje: number
  generos_mas_jugados: { juego__genero: string; total: number }[]
}

export const userJuegoService = {
  async listMios(): Promise<ApiResponse<UserJuego[]>> {
    const { data } = await api.get<ApiResponse<UserJuego[]>>('/juegos/mis-juegos/')
    return data
  },

  async unirse(payload: UnirseAJuegoPayload): Promise<ApiResponse<UserJuego>> {
    const { data } = await api.post<ApiResponse<UserJuego>>('/juegos/mis-juegos/', payload)
    return data
  },

  async actualizar(id: number, payload: ActualizarUserJuegoPayload): Promise<ApiResponse<UserJuego>> {
    const { data } = await api.patch<ApiResponse<UserJuego>>(`/juegos/mis-juegos/${id}/`, payload)
    return data
  },

  async salir(id: number): Promise<void> {
    await api.delete(`/juegos/mis-juegos/${id}/`)
  },

  async estadisticas(): Promise<ApiResponse<EstadisticasUsuario>> {
    const { data } = await api.get<ApiResponse<EstadisticasUsuario>>('/juegos/mis-juegos/estadisticas/')
    return data
  },
}