<script setup lang="ts">
defineProps<{
    variant?: 'primary' | 'secondary' | 'danger'
    disabled?: boolean
    type?: 'button' | 'submit'
}>()

defineEmits<{
    click: [event: MouseEvent]
}>()
</script>

<template>
    <button :type="type ?? 'button'" :disabled="disabled" class="app-button"
        :class="`app-button--${variant ?? 'primary'}`" @click="$emit('click', $event)">
        <slot />
    </button>
</template>

<style scoped>
.app-button {
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    border: none;
    font-weight: bold;
    font-family: var(--font-sans);
    font-size: var(--font-size-base);
    cursor: pointer;
    transition: transform 0.15s ease, filter 0.15s ease, opacity 0.15s ease;
}

.app-button--primary {
    background: var(--color-header-bg);
    color: var(--color-header-text);
}

.app-button--secondary {
    background: transparent;
    color: var(--color-text);
    border: 1px solid var(--color-text-secondary);
}

.app-button--danger {
    background: transparent;
    color: #ff6b6b;
    border: 1px solid #ff6b6b;
}

.app-button:hover:not(:disabled) {
    filter: brightness(1.1);
    transform: translateY(-1px);
}

.app-button:active:not(:disabled) {
    transform: scale(0.97);
}

.app-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

@media (max-width: 480px) {
    .app-button {
        width: 100%;
    }
}
</style>