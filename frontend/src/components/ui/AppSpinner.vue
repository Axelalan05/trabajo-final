<script setup lang="ts">
withDefaults(defineProps<{
    texto?: string
}>(), {
    texto: 'Cargando...',
})
</script>

<template>
    <div class="spinner-wrapper">
        <div class="spinner"></div>
        <p v-if="texto" class="spinner-texto">{{ texto }}</p>
    </div>
</template>

<style scoped>
.spinner-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: var(--space-3);
    padding: var(--space-8) 0;
}

.spinner {
    width: 42px;
    height: 42px;
    border: 4px solid rgba(255, 255, 255, 0.15);
    border-top-color: var(--color-header-bg);
    border-radius: var(--radius-full);
    animation: girar 0.8s linear infinite;
}

.spinner-texto {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin: 0;
}

@keyframes girar {
    to {
        transform: rotate(360deg);
    }
}
</style>