<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { juegoService } from '@/services/juegoService'
import type { Juego } from '@/types'
import { onMounted, ref } from 'vue'

const juegos = ref<Juego[]>([])
const loading = ref(true)
const genero = ref('')
const plataforma = ref('')
const estado = ref('')
const ordering = ref('-created_at')

async function cargarJuegos() {
    loading.value = true
    try {
        const response = await juegoService.listPublico({
            genero: genero.value || undefined,
            plataforma: plataforma.value || undefined,
            estado: estado.value || undefined,
            ordering: ordering.value,
        })
        juegos.value = response.data
    } finally {
        loading.value = false
    }
}

onMounted(cargarJuegos)
</script>

<template>
    <div class="explorar-view">
        <h1>Explorar juegos</h1>

        <div class="filtros">
            <input v-model="genero" placeholder="Género" @keyup.enter="cargarJuegos" />
            <input v-model="plataforma" placeholder="Plataforma" @keyup.enter="cargarJuegos" />
            <select v-model="estado">
                <option value="">Todos los estados</option>
                <option value="jugando">Jugando</option>
                <option value="completado">Completado</option>
                <option value="pendiente">Pendiente</option>
                <option value="abandonado">Abandonado</option>
            </select>
            <select v-model="ordering">
                <option value="-created_at">Más recientes</option>
                <option value="-puntaje">Mejor puntaje</option>
                <option value="nombre">Nombre (A-Z)</option>
            </select>
            <AppButton @click="cargarJuegos">Filtrar</AppButton>
        </div>

        <div v-if="loading">Cargando...</div>

        <div v-else-if="juegos.length === 0" class="vacio">
            No se encontraron juegos.
        </div>

        <div v-else class="lista-juegos">
            <div v-for="juego in juegos" :key="juego.id" class="juego-card">
                <h3>{{ juego.nombre }}</h3>
                <p class="detalle">{{ juego.genero }} · {{ juego.plataforma }} · {{ juego.anio }}</p>
                <p class="estado">{{ juego.estado }}</p>
                <p v-if="juego.puntaje" class="puntaje">⭐ {{ juego.puntaje }}/10</p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.explorar-view {
    max-width: 900px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
}

.filtros {
    display: flex;
    gap: var(--space-2);
    margin-bottom: var(--space-6);
    flex-wrap: wrap;
}

.filtros input,
.filtros select {
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
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