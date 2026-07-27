import { reactive } from 'vue'

export type ToastType = 'success' | 'error' | 'info' | 'warning'

export interface Toast {
  id: number
  message: string
  type: ToastType
  icon?: string
}

const state = reactive({
  toasts: [] as Toast[]
})

let nextId = 0

export function useToast() {
  function addToast(message: string, type: ToastType = 'info', icon?: string) {
    const id = nextId++
    state.toasts.push({ id, message, type, icon })
    setTimeout(() => removeToast(id), 4000)
  }

  function removeToast(id: number) {
    const idx = state.toasts.findIndex(t => t.id === id)
    if (idx !== -1) {
      state.toasts.splice(idx, 1)
    }
  }

  return {
    toasts: state.toasts,
    addToast,
    removeToast,
  }
}
