<script setup lang="ts">
import { X } from 'lucide-vue-next';
import { Teleport } from 'vue';

defineProps<{
    show: boolean
    title: string
}>()

defineEmits<{
    close: []
}>()
</script>

<template>
    <Teleport to="body">
        <Transition name="fade">
            <div v-if="show" class="overlay" @click.self="$emit('close')">
                <div class="modal">
                    <div class="modal-header">
                        <h2>{{ title }}</h2>
                        <button class="close-btn" @click="$emit('close')">
                            <X :size="20" />
                        </button>
                    </div>
                    <div class="modal-body">
                        <slot />
                    </div>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<style scoped>
.overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: var(--space-4);
}

.modal {
    background: var(--color-footer-bg);
    color: var(--color-text);
    border-radius: var(--radius-lg);
    padding: var(--space-6);
    max-width: 480px;
    width: 100%;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--space-4);
}

.close-btn {
    background: transparent;
    border: none;
    color: var(--color-text-secondary);
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: color 0.15s ease;
}

.close-btn:hover {
    color: var(--color-text);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>