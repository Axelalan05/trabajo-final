<script setup lang="ts">
import AppFooter from '@/components/ui/AppFooter.vue';
import AppHeader from '@/components/ui/AppHeader.vue';
import BackToTop from '@/components/ui/BackToTop.vue';
</script>

<template>
    <div class="app-layout">
        <AppHeader />
        <main class="contenido">
            <slot />
        </main>
        <AppFooter />
        <BackToTop />
    </div>
</template>

<style scoped>
.app-layout {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

.contenido {
    flex: 1;
    position: relative;
    z-index: 0;
    background: var(--color-bg);
}

.contenido::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image: url('@/assets/background-juegos.svg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.15;
    z-index: -1;
    pointer-events: none;
}
</style>