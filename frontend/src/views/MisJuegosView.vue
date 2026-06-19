<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { juegoService } from '@/services/juegoService'
import type { Juego } from '@/types'
import { onMounted, ref } from 'vue'

const juegos = ref<Juego[]>([])
const loading = ref(true)

async function cargarJuegos() {
    loading.value = true
    try {
        const response = await juegoService.listMios()
        juegos.value = response.data
    } finally {
        loading.value = false
    }
}

async function eliminarJuego(id: number) {
    if (!confirm('¿Seguro que querés eliminar este juego?')) return
    await juegoService.delete(id)
    juegos.value = juegos.value.filter((j) => j.id !== id)
}

onMounted(cargarJuegos)
</script>

<template>
    <div class="mis-juegos-view">
        <h1>Mi colección</h1>

        <div v-if="loading">Cargando...</div>

        <div v-else-if="juegos.length === 0" class="vacio">
            Todavía no agregaste ningún juego.
        </div>

        <div v-else class="lista-juegos">
            <div v-for="juego in juegos" :key="juego.id" class="juego-card">
                <h3>{{ juego.nombre }}</h3>
                <p class="detalle">{{ juego.genero }} · {{ juego.plataforma }} · {{ juego.anio }}</p>
                <p class="estado">{{ juego.estado }}</p>
                <p v-if="juego.puntaje" class="puntaje">⭐ {{ juego.puntaje }}/10</p>
                <AppButton class="boton-eliminar" @click="eliminarJuego(juego.id)">Eliminar</AppButton>
            </div>
        </div>
    </div>
</template>

<style scoped>
.mis-juegos-view {
    max-width: 900px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
}

.vacio {
    color: var(--color-text-secondary);
    text-align: center;
    margin-top: var(--space-8);
}

.lista-juegos {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: var(--space-4);
}

.juego-card {
    background: var(--color-footer-bg);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    text-align: left;
}

.detalle {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
}

.estado {
    color: var(--color-header-bg);
    font-weight: bold;
    margin-top: var(--space-2);
}

.puntaje {
    margin-top: var(--space-2);
}
</style>