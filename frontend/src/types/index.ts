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
  nombre: string
  genero: string
  plataforma: string
  imagen: string | null
  descripcion: string
  anio: number
  created_at: string
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