<script setup lang="ts">
import logo from '@/assets/logo.svg'
import { useAuthStore } from '@/stores/auth'
import { ChevronDown, LogOut, UserCircle, UserRound } from 'lucide-vue-next'
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const showMenu = ref(false)
const menuRef = ref<HTMLElement | null>(null)

function toggleMenu() {
    showMenu.value = !showMenu.value
}

function cerrarMenu() {
    showMenu.value = false
}

async function handleLogout() {
    cerrarMenu()
    await authStore.logout()
    router.push('/login')
}

function handleClickFuera(event: MouseEvent) {
    if (menuRef.value && !menuRef.value.contains(event.target as Node)) {
        showMenu.value = false
    }
}

onMounted(() => {
    document.addEventListener('click', handleClickFuera)
})

onUnmounted(() => {
    document.removeEventListener('click', handleClickFuera)
})
</script>

<template>
    <header class="app-header">
        <router-link to="/" class="logo-link">
            <img :src="logo" alt="GameVault" class="logo-img" />
        </router-link>

        <nav class="nav">
            <router-link to="/explorar">Explorar</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/mis-juegos">Mi colección</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin/juegos">Administrar catálogo</router-link>

            <div v-if="authStore.isAuthenticated" class="perfil-menu" ref="menuRef">
                <button class="perfil-btn" @click="toggleMenu">
                    <UserCircle :size="22" />
                    <ChevronDown :size="16" />
                </button>

                <div v-if="showMenu" class="dropdown">
                    <router-link to="/perfil" class="dropdown-item" @click="cerrarMenu">
                        <UserRound :size="18" /> Perfil
                    </router-link>
                    <button class="dropdown-item dropdown-item-btn" @click="handleLogout">
                        <LogOut :size="18" /> Cerrar sesión
                    </button>
                </div>
            </div>

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

.login-link:hover {
    background: rgba(18, 19, 102, 0.1);
    transform: translateY(-1px);
}

.perfil-menu {
    position: relative;
}

.perfil-btn {
    background: transparent;
    border: 1px solid var(--color-header-text);
    color: var(--color-header-text);
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-md);
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: var(--space-1);
    transition: background 0.15s ease, transform 0.15s ease;
}

.perfil-btn:hover {
    background: rgba(18, 19, 102, 0.1);
    transform: translateY(-1px);
}

.dropdown {
    position: absolute;
    top: calc(100% + var(--space-2));
    right: 0;
    background: var(--color-footer-bg);
    border-radius: var(--radius-md);
    overflow: hidden;
    min-width: 160px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    z-index: 10;
    display: flex;
    flex-direction: column;
}

.dropdown-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    width: 100%;
    text-align: left;
    padding: var(--space-2) var(--space-3);
    background: transparent;
    border: none;
    cursor: pointer;
    font-size: var(--font-size-base);
    font-family: var(--font-sans);
    text-decoration: none;
    transition: background 0.15s ease;
}

.dropdown .dropdown-item {
    color: var(--color-text);
}

.dropdown-item:hover {
    background: rgba(255, 255, 255, 0.08);
}

.dropdown-item-btn {
    color: #ff6b6b !important;
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