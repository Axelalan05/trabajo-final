export interface User {
  id: number
  username: string
  email: string
  date_joined: string
  is_staff: boolean
}

export interface Profile {
  username: string
  email?: string
  bio: string
  avatar: string | null
}

// Catálogo: ya no tiene estado/puntaje/reseña/favorito — eso es de cada usuario
export interface Juego {
  id: number
  rawg_id: number | null
  nombre: string
  genero: string
  plataforma: string
  imagen_url: string | null
  descripcion: string
  fecha_lanzamiento: string | null
  created_at: string
}

export interface RawgResultado {
  rawg_id: number
  nombre: string
  imagen_url: string | null
  fecha_lanzamiento: string | null
  genero: string
  plataforma: string
}

export interface RawgDetalle extends RawgResultado {
  descripcion: string
}

export type EstadoJuego = 'jugando' | 'completado' | 'pendiente' | 'abandonado'

// La relación de "mi cuenta" con un juego del catálogo
export interface UserJuego {
  id: number
  juego: Juego
  estado: EstadoJuego
  puntaje: number | null
  resenia: string
  created_at: string
}

export interface ApiResponse<T> {
  success: boolean
  data: T
  message?: string
}

export interface ApiError {
  success: false
  error: {
    code: string
    message: string
    details?: Record<string, string[]>
  }
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface JuegoDetalleResponse {
  juego: Juego
  puntaje_promedio: number | null
  total_resenias: number
  mi_user_juego: UserJuego | null
}
