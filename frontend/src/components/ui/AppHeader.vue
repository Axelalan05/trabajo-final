<script setup lang="ts">
import logo from '@/assets/logo.svg'
import { useAuthStore } from '@/stores/auth'
import { ChevronDown, LogOut, Menu, UserCircle, UserRound, X } from 'lucide-vue-next'
import { onMounted, onUnmounted, ref } from 'vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

// Menú de perfil (desktop)
const showMenu = ref(false)
const menuRef = ref<HTMLElement | null>(null)

// Menú hamburguesa (mobile)
const showMobileMenu = ref(false)
const showMobilePerfilSubmenu = ref(false)

function toggleMenu() {
    showMenu.value = !showMenu.value
}

function cerrarMenu() {
    showMenu.value = false
}

function toggleMobileMenu() {
    showMobileMenu.value = !showMobileMenu.value
    if (!showMobileMenu.value) {
        showMobilePerfilSubmenu.value = false
    }
}

function cerrarMobileMenu() {
    showMobileMenu.value = false
    showMobilePerfilSubmenu.value = false
}

function toggleMobilePerfilSubmenu() {
    showMobilePerfilSubmenu.value = !showMobilePerfilSubmenu.value
}

function handleOverlayClick() {
    cerrarMobileMenu()
}

async function handleLogout() {
    cerrarMenu()
    cerrarMobileMenu()
    await authStore.logout()
    router.push('/login')
}

// Solo para el dropdown de perfil en desktop
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

        <!-- Navegación desktop -->
        <nav class="nav-desktop">
            <router-link to="/" class="nav-inicio">Inicio</router-link>
            <router-link to="/explorar">Explorar</router-link>
            <router-link v-if="authStore.isAuthenticated" to="/mis-juegos">Mi colección</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin/juegos">Administrar catálogo</router-link>
            <router-link v-if="authStore.isAdmin" to="/admin/usuarios">Administrar usuarios</router-link>

            <div v-if="authStore.isAuthenticated" class="perfil-menu" ref="menuRef">
                <button class="perfil-btn" @click="toggleMenu">
                    <UserCircle :size="22" />
                    <ChevronDown :size="16" />
                </button>

                <Transition name="dropdown">
                    <div v-if="showMenu" class="dropdown">
                        <router-link to="/perfil" class="dropdown-item" @click="cerrarMenu">
                            <UserRound :size="18" /> Perfil
                        </router-link>
                        <button class="dropdown-item dropdown-item-btn" @click="handleLogout">
                            <LogOut :size="18" /> Cerrar sesión
                        </button>
                    </div>
                </Transition>
            </div>

            <router-link v-else to="/login" class="login-link">Ingresar</router-link>
        </nav>

        <!-- Botón hamburguesa (mobile) -->
        <button class="hamburger-btn" @click="toggleMobileMenu" aria-label="Menú de navegación">
            <Menu v-if="!showMobileMenu" :size="28" />
            <X v-else :size="28" />
        </button>

        <!-- Overlay oscuro -->
        <div v-if="showMobileMenu" class="mobile-overlay" @click="handleOverlayClick"></div>

        <!-- Menú mobile desplegable -->
        <Transition name="mobile-menu">
            <div v-if="showMobileMenu" class="mobile-menu">
                <router-link to="/" class="mobile-item" @click="cerrarMobileMenu">Inicio</router-link>
                <router-link to="/explorar" class="mobile-item" @click="cerrarMobileMenu">Explorar</router-link>
                <router-link v-if="authStore.isAuthenticated" to="/mis-juegos" class="mobile-item"
                    @click="cerrarMobileMenu">Mi colección</router-link>
                <router-link v-if="authStore.isAdmin" to="/admin/juegos" class="mobile-item"
                    @click="cerrarMobileMenu">Administrar catálogo</router-link>
                <router-link v-if="authStore.isAdmin" to="/admin/usuarios" class="mobile-item"
                    @click="cerrarMobileMenu">Administrar usuarios</router-link>

                <template v-if="authStore.isAuthenticated">
                    <div class="mobile-perfil-section">
                        <button class="mobile-item mobile-perfil-btn" @click="toggleMobilePerfilSubmenu">
                            <UserRound :size="18" /> Perfil
                            <ChevronDown :size="16" class="chevron-perfil"
                                :class="{ 'chevron-abierto': showMobilePerfilSubmenu }" />
                        </button>
                        <div v-if="showMobilePerfilSubmenu" class="mobile-submenu">
                            <router-link to="/perfil" class="mobile-subitem" @click="cerrarMobileMenu">
                                <UserRound :size="16" /> Mi perfil
                            </router-link>
                            <button class="mobile-subitem mobile-subitem-danger" @click="handleLogout">
                                <LogOut :size="16" /> Cerrar sesión
                            </button>
                        </div>
                    </div>
                </template>

                <router-link v-else to="/login" class="mobile-item mobile-login"
                    @click="cerrarMobileMenu">Ingresar</router-link>
            </div>
        </Transition>
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
    gap: var(--space-4);
    position: sticky;
    top: 0;
    z-index: 100;
}

.logo-link {
    display: flex;
    align-items: center;
    flex-shrink: 0;
}

.logo-img {
    height: 40px;
}

/* ===== Navegación desktop ===== */
.nav-desktop {
    display: flex;
    align-items: center;
    gap: var(--space-4);
}

.nav-desktop a {
    color: var(--color-header-text);
    text-decoration: none;
    font-weight: 500;
    white-space: nowrap;
    transition: opacity 0.15s ease;
}

.nav-desktop a:hover {
    opacity: 0.7;
}

.nav-desktop a.router-link-active {
    text-decoration: underline;
}

.nav-inicio {
    font-weight: 800;
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

/* Menú desplegable perfil (desktop) */
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
    z-index: 101;
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

/* ===== Botón hamburguesa (mobile) ===== */
.hamburger-btn {
    display: none;
    background: transparent;
    border: 1px solid var(--color-header-text);
    color: var(--color-header-text);
    padding: var(--space-1);
    border-radius: var(--radius-md);
    cursor: pointer;
    line-height: 0;
    transition: background 0.15s ease;
    z-index: 102;
    flex-shrink: 0;
}

.hamburger-btn:hover {
    background: rgba(18, 19, 102, 0.1);
}

/* ===== Overlay oscuro ===== */
.mobile-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(0, 0, 0, 0.6);
    z-index: 98;
}

/* ===== Menú mobile ===== */
.mobile-menu {
    position: absolute;
    top: 100%;
    left: 0;
    width: 100%;
    background: var(--color-footer-bg);
    border-radius: 0 0 var(--radius-md) var(--radius-md);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    z-index: 99;
    display: flex;
    flex-direction: column;
    padding: var(--space-2) 0;
}

.mobile-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-6);
    color: var(--color-text);
    text-decoration: none;
    font-size: var(--font-size-base);
    font-family: var(--font-sans);
    background: transparent;
    border: none;
    text-align: left;
    cursor: pointer;
    transition: background 0.15s ease;
    width: 100%;
    box-sizing: border-box;
}

.mobile-item:hover {
    background: rgba(255, 255, 255, 0.08);
}

.mobile-item.router-link-active {
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid var(--color-header-bg);
}

.mobile-login {
    color: var(--color-header-bg) !important;
    font-weight: bold;
}

/* Submenú perfil dentro del menú mobile */
.mobile-perfil-section {
    display: flex;
    flex-direction: column;
}

.mobile-perfil-btn {
    justify-content: space-between;
}

.chevron-perfil {
    transition: transform 0.2s ease;
    flex-shrink: 0;
}

.chevron-abierto {
    transform: rotate(180deg);
}

.mobile-submenu {
    display: flex;
    flex-direction: column;
    background: rgba(0, 0, 0, 0.2);
}

.mobile-subitem {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-6) var(--space-2) calc(var(--space-6) + var(--space-4));
    color: var(--color-text);
    text-decoration: none;
    font-size: var(--font-size-sm);
    font-family: var(--font-sans);
    background: transparent;
    border: none;
    text-align: left;
    cursor: pointer;
    transition: background 0.15s ease;
    width: 100%;
    box-sizing: border-box;
}

.mobile-subitem:hover {
    background: rgba(255, 255, 255, 0.08);
}

.mobile-subitem-danger {
    color: #ff6b6b !important;
}

.dropdown-enter-active,
.dropdown-leave-active {
    transition: transform 0.2s ease, opacity 0.2s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
    transform: translateY(-8px);
    opacity: 0;
}

/* ===== Responsive ===== */
@media (min-width: 769px) {
    .mobile-menu {
        display: none !important;
    }

    .mobile-overlay {
        display: none !important;
    }
}

@media (max-width: 768px) {
    .nav-desktop {
        display: none !important;
    }

    .hamburger-btn {
        display: flex;
    }

    .app-header {
        padding: var(--space-3) var(--space-4);
    }

    .mobile-item:active {
        background: var(--color-header-bg);
        color: var(--color-header-text);
    }

    .mobile-subitem:active {
        background: var(--color-header-bg);
        color: var(--color-header-text);
    }

    .mobile-item:active .mobile-login,
    .mobile-login:active {
        color: var(--color-header-text) !important;
    }

    .mobile-subitem.mobile-subitem-danger:active {
        background: var(--color-header-bg);
        color: var(--color-header-text) !important;
    }

    .mobile-menu-enter-active,
    .mobile-menu-leave-active {
        transition: transform 0.25s ease, opacity 0.25s ease;
    }

    .mobile-menu-enter-from,
    .mobile-menu-leave-to {
        transform: translateY(-10px);
        opacity: 0;
    }
}
</style>
