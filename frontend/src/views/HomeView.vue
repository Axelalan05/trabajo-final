<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import { Boxes, Database, Facebook, Gamepad2, Instagram, Server, Twitter, Youtube } from 'lucide-vue-next';

const authStore = useAuthStore()

const redes = [
    { nombre: 'Facebook', url: 'https://www.facebook.com/axeldavid.alan/', icon: Facebook },
    { nombre: 'Instagram', url: 'https://www.instagram.com/axelalan_05/', icon: Instagram },
    { nombre: 'YouTube', url: 'https://www.youtube.com/channel/UC9cfLZ6zf6Y47lCcmlEkckA', icon: Youtube },
    { nombre: 'Twitter', url: 'https://x.com/AxelitoalanOK', icon: Twitter },
]
</script>

<template>
    <div class="home-view">
        <section class="hero">
            <h1 class="titulo-hero">
                <Gamepad2 :size="36" />
                GameVault
                <Gamepad2 :size="36" />
            </h1>
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

            <div class="redes">

                <a v-for="red in redes" :key="red.nombre" :href="red.url" target="_blank" rel="noopener noreferrer"
                    :aria-label="red.nombre" class="red-link">
                    <component :is="red.icon" :size="22" />
                </a>
            </div>
        </section>

        <section class="presentacion">
            <h2>Sobre este proyecto</h2>
            <p class="texto-presentacion">
                Soy Axel, estudiante de la Universidad Nacional del Comahue, y GameVault es mi proyecto final
                para la materia Frameworks e Interoperabilidad. La idea es simple: un catálogo de juegos que yo,
                como administrador, mantengo curado y sin duplicados, donde cada usuario puede sumar los juegos
                que le interesan a su propia colección y llevar el registro de en qué estado está cada uno
                (pendiente, jugando, completado o abandonado).
            </p>

            <div class="stack">
                <div class="stack-item">
                    <Server :size="28" />
                    <div>
                        <p class="stack-titulo">Backend</p>
                        <p class="stack-detalle">Django + Django REST Framework, autenticación con JWT</p>
                    </div>
                </div>
                <div class="stack-item">
                    <Gamepad2 :size="28" />
                    <div>
                        <p class="stack-titulo">Frontend</p>
                        <p class="stack-detalle">Vue 3 + TypeScript, con Pinia para el estado global</p>
                    </div>
                </div>
                <div class="stack-item">
                    <Database :size="28" />
                    <div>
                        <p class="stack-titulo">Base de datos</p>
                        <p class="stack-detalle">PostgreSQL, todo orquestado con Docker Compose</p>
                    </div>
                </div>
                <div class="stack-item">
                    <Boxes :size="28" />
                    <div>
                        <p class="stack-titulo">Datos de juegos</p>
                        <p class="stack-detalle">
                            API de <strong>RAWG</strong> (rawg.io): trae la portada, la descripción, el género,
                            las plataformas y la fecha de lanzamiento real de cada juego del catálogo.
                        </p>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.home-view {
    padding: var(--space-8);
    color: var(--color-text);
}

.hero {
    text-align: center;
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

.redes {
    display: flex;
    gap: var(--space-3);
    justify-content: center;
    margin-top: var(--space-6);
}

.red-link {
    color: var(--color-text);
    background: var(--color-footer-bg);
    width: 40px;
    height: 40px;
    border-radius: var(--radius-full);
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform 0.15s ease, background 0.15s ease;
}

.red-link:hover {
    transform: translateY(-2px);
    background: var(--color-header-bg);
    color: var(--color-header-text);
}

.presentacion {
    max-width: 800px;
    margin: var(--space-8) auto 0;
    background: var(--color-footer-bg);
    border-radius: var(--radius-md);
    padding: var(--space-6);
    text-align: left;
}

.presentacion h2 {
    margin-top: 0;
    text-align: center;
}

.texto-presentacion {
    color: var(--color-text-secondary);
    line-height: 1.6;
}

.stack {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: var(--space-4);
    margin-top: var(--space-6);
}

.stack-item {
    display: flex;
    gap: var(--space-3);
    align-items: flex-start;
    flex: 1 1 220px;
    max-width: 340px;
}

.stack-item svg {
    flex-shrink: 0;
    color: var(--color-header-bg);
    margin-top: 2px;
}

.stack-titulo {
    font-weight: bold;
    margin: 0 0 var(--space-1);
}

.stack-detalle {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin: 0;
}

.titulo-hero {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-3);
}

.titulo-hero svg {
    color: var(--color-header-bg);
}
</style>