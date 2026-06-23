<script setup lang="ts">
import AppFooter from '@/components/ui/AppFooter.vue';
import AppHeader from '@/components/ui/AppHeader.vue';
</script>

<template>
    <div class="app-layout">
        <AppHeader />
        <main class="contenido">
            <slot />
        </main>
        <AppFooter />
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
}
</style>