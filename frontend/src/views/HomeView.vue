<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore()
</script>

<template>
    <div class="home-view">
        <h1>GameVault</h1>
        <p>Tu biblioteca personal de videojuegos</p>
        <div class="acciones">
            <router-link v-if="!authStore.isAuthenticated" to="/login" class="boton">
                Iniciar sesión
            </router-link>
            <router-link v-if="!authStore.isAuthenticated" to="/register" class="boton boton-secundario">
                Registrarme
            </router-link>
            <router-link v-if="authStore.isAuthenticated" to="/mis-juegos" class="boton">
                Mi colección
            </router-link>
            <router-link to="/explorar" class="boton boton-secundario">
                Explorar juegos
            </router-link>
        </div>
    </div>
</template>

<style scoped>
.home-view {
    text-align: center;
    padding: var(--space-8);
    color: var(--color-text);
}

.acciones {
    display: flex;
    gap: var(--space-4);
    justify-content: center;
    margin-top: var(--space-6);
    flex-wrap: wrap;
}

.boton {
    background: var(--color-header-bg);
    color: var(--color-header-text);
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    text-decoration: none;
    font-weight: bold;
    transition: transform 0.15s ease, filter 0.15s ease;
}

.boton:hover {
    filter: brightness(1.1);
    transform: translateY(-1px);
}

.boton:active {
    transform: scale(0.97);
}

.boton-secundario {
    background: transparent;
    color: var(--color-text);
    border: 1px solid var(--color-text-secondary);
}
</style>