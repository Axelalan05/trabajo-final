<script setup lang="ts">
import { useToast } from '@/stores/toast'
import { AlertTriangle, CheckCircle, Info, LogOut, MessageSquare, Pencil, Plus, RefreshCw, Star, Trash2, UserPlus, UserX, XCircle } from 'lucide-vue-next'
import type { Component } from 'vue'

const { toasts, removeToast } = useToast()

const iconMap: Record<string, Component> = {
  plus: Plus,
  pencil: Pencil,
  trash2: Trash2,
  userX: UserX,
  userPlus: UserPlus,
  logOut: LogOut,
  star: Star,
  refreshCw: RefreshCw,
  messageSquare: MessageSquare,
}

const defaultIcons: Record<string, Component> = {
  success: CheckCircle,
  error: XCircle,
  info: Info,
  warning: AlertTriangle,
}

function getIcon(toast: { type: string; icon?: string }) {
  if (toast.icon && iconMap[toast.icon]) return iconMap[toast.icon]
  return defaultIcons[toast.type] || Info
}
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="toast">
      <div v-for="toast in toasts" :key="toast.id" :class="['toast', `toast--${toast.type}`]" @click="removeToast(toast.id)">
        <component :is="getIcon(toast)" :size="20" class="toast-icon" />
        <span class="toast-message">{{ toast.message }}</span>
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: calc(72px + var(--space-3));
  right: var(--space-4);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  pointer-events: none;
  max-width: 360px;
  width: 100%;
}

.toast {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  background: var(--color-footer-bg);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
  cursor: pointer;
  pointer-events: auto;
  font-size: var(--font-size-sm);
}

.toast--success {
  border-left: 4px solid #22c55e;
}
.toast--error {
  border-left: 4px solid #ef4444;
}
.toast--info {
  border-left: 4px solid #3b82f6;
}
.toast--warning {
  border-left: 4px solid #f59e0b;
}

.toast-icon {
  flex-shrink: 0;
}

.toast--success .toast-icon {
  color: #22c55e;
}
.toast--error .toast-icon {
  color: #ef4444;
}
.toast--info .toast-icon {
  color: #3b82f6;
}
.toast--warning .toast-icon {
  color: #f59e0b;
}

.toast-message {
  flex: 1;
}

.toast-enter-active {
  transition: all 0.3s ease;
}
.toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from {
  transform: translateX(100%);
  opacity: 0;
}
.toast-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

@media (max-width: 480px) {
  .toast-container {
    left: var(--space-4);
    right: var(--space-4);
    max-width: none;
  }
}
</style>
