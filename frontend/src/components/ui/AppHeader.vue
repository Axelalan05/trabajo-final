<script setup lang="ts">
import logo from '@/assets/logo.svg'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogout() {
    await authStore.logout()
    router.push('/login')
}
</script>

<template>
    <header class="app-header">
        <router-link to="/" class="logo-link">
            <img :src="logo" alt="GameVault" class="logo-img" />
        </router-link>

        <nav class="nav">
            <router-link to="/explorar">Explorar</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/mis-juegos">Mi colección</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/perfil">Perfil</router-link>

            <button v-if="authStore.isAuthenticated" class="logout-btn" @click="handleLogout">
                Cerrar sesión
            </button>
            <router-link v-else to="/login" class="login-link">Ingresar</router-link>
        </nav>
    </header>
</template>

<style scoped>
.app-header {
    background: var(--color-header-bg);
    color: var(--color-header-text);
    padding: var(--space-4) var(--space-6);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-4);
}

.logo {
    font-size: var(--font-size-xl);
    font-weight: bold;
    color: var(--color-header-text);
    text-decoration: none;
}

.nav {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    flex-wrap: wrap;
}

.nav a {
    color: var(--color-header-text);
    text-decoration: none;
    font-weight: 500;
    transition: opacity 0.15s ease;
}

.nav a:hover {
    opacity: 0.7;
}

.nav a.router-link-active {
    text-decoration: underline;
}

.logout-btn,
.login-link {
    background: transparent;
    border: 1px solid var(--color-header-text);
    color: var(--color-header-text);
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-weight: bold;
    transition: background 0.15s ease, transform 0.15s ease;
}

.logout-btn:hover,
.login-link:hover {
    background: rgba(18, 19, 102, 0.1);
    transform: translateY(-1px);
}

@media (max-width: 600px) {
    .app-header {
        flex-direction: column;
        align-items: flex-start;
    }

    .nav {
        width: 100%;
        justify-content: space-between;
    }
}

.logo-link {
    display: flex;
    align-items: center;
}

.logo-img {
    height: 40px;
}
</style>