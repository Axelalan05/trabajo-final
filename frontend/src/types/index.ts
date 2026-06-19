export interface User {
  id: number
  username: string
  email: string
  date_joined: string
}

export interface Profile {
  username: string
  email?: string
  bio: string
  avatar: string | null
}

export interface Juego {
  id: number
  nombre: string
  genero: string
  plataforma: string
  imagen: string | null
  descripcion: string
  anio: number
  estado: 'jugando' | 'completado' | 'pendiente' | 'abandonado'
  puntaje: number | null
  reseña: string
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