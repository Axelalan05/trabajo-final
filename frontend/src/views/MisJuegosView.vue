<script setup lang="ts">
import JuegoForm from '@/components/juegos/JuegoForm.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import { juegoService } from '@/services/juegoService'
import type { Juego } from '@/types'
import { Heart, Pencil, Plus, Star, Trash2 } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'

const juegos = ref<Juego[]>([])
const loading = ref(true)
const showModal = ref(false)
const juegoEditando = ref<Juego | null>(null)
const errorSubmit = ref('')
const estadisticas = ref<{
    juegos_completados: number
    promedio_puntaje: number
    generos_mas_jugados: { genero: string; total: number }[]
} | null>(null)

async function cargarJuegos() {
    loading.value = true
    try {
        const response = await juegoService.listMios()
        juegos.value = response.data
    } finally {
        loading.value = false
    }
}

async function cargarEstadisticas() {
    try {
        const response = await juegoService.estadisticas()
        estadisticas.value = response.data
    } catch {
        // silencioso
    }
}

function abrirModalCrear() {
    juegoEditando.value = null
    errorSubmit.value = ''
    showModal.value = true
}

function abrirModalEditar(juego: Juego) {
    juegoEditando.value = juego
    errorSubmit.value = ''
    showModal.value = true
}

function cerrarModal() {
    showModal.value = false
    juegoEditando.value = null
    errorSubmit.value = ''
}

async function handleSubmit(data: Partial<Juego>) {
    errorSubmit.value = ''
    try {
        if (juegoEditando.value) {
            await juegoService.update(juegoEditando.value.id, data)
        } else {
            await juegoService.create(data)
        }
        cerrarModal()
        await cargarJuegos()
        await cargarEstadisticas()
    } catch (err: any) {
        const detail = err?.response?.data?.error?.details
        if (detail && typeof detail === 'object') {
            const mensajes = Object.values(detail).flat()
            errorSubmit.value = (mensajes as string[]).join(' ')
        } else {
            errorSubmit.value = 'Error al guardar el juego.'
        }
    }
}

async function eliminarJuego(id: number) {
    if (!confirm('¿Seguro que querés eliminar este juego?')) return
    await juegoService.delete(id)
    juegos.value = juegos.value.filter((j) => j.id !== id)
    await cargarEstadisticas()
}

async function toggleFavorito(juego: Juego) {
    await juegoService.toggleFavorito(juego.id)
    juego.es_favorito = !juego.es_favorito
}

onMounted(async () => {
    await cargarJuegos()
    await cargarEstadisticas()
})
</script>

<template>
    <div class="mis-juegos-view">
        <div class="encabezado">
            <h1>Mi colección</h1>
            <AppButton @click="abrirModalCrear">
                <Plus :size="18" /> Agregar juego
            </AppButton>
        </div>

        <div v-if="estadisticas" class="estadisticas">
            <div class="stat-card">
                <p class="stat-numero">{{ juegos.length }}</p>
                <p class="stat-label">Total de juegos</p>
            </div>
            <div class="stat-card">
                <p class="stat-numero">{{ estadisticas.juegos_completados }}</p>
                <p class="stat-label">Completados</p>
            </div>
            <div class="stat-card">
                <p class="stat-numero">{{ estadisticas.promedio_puntaje }}</p>
                <p class="stat-label">Puntaje promedio</p>
            </div>
            <div class="stat-card">
                <p class="stat-numero">{{ estadisticas.generos_mas_jugados[0]?.genero ?? '—' }}</p>
                <p class="stat-label">Género favorito</p>
            </div>
        </div>

        <div v-if="loading">Cargando...</div>

        <div v-else-if="juegos.length === 0" class="vacio">
            Todavía no agregaste ningún juego.
        </div>

        <div v-else class="lista-juegos">
            <div v-for="juego in juegos" :key="juego.id" class="juego-card">
                <div class="card-top">
                    <h3>{{ juego.nombre }}</h3>
                    <button class="favorito-btn" :class="{ activo: juego.es_favorito }" @click="toggleFavorito(juego)">
                        <Heart :size="20" :fill="juego.es_favorito ? 'currentColor' : 'none'" />
                    </button>
                </div>
                <p class="detalle">{{ juego.genero }} · {{ juego.plataforma }} · {{ juego.anio }}</p>
                <p class="estado">{{ juego.estado }}</p>
                <p v-if="juego.puntaje" class="puntaje">
                    <Star :size="16" /> {{ juego.puntaje }}/10
                </p>
                <div class="acciones">
                    <button class="icon-btn" @click="abrirModalEditar(juego)">
                        <Pencil :size="18" />
                    </button>
                    <button class="icon-btn icon-btn-danger" @click="eliminarJuego(juego.id)">
                        <Trash2 :size="18" />
                    </button>
                </div>
            </div>
        </div>

        <AppModal :show="showModal" :title="juegoEditando ? 'Editar juego' : 'Agregar juego'" @close="cerrarModal">
            <p v-if="errorSubmit" class="error-modal">{{ errorSubmit }}</p>
            <JuegoForm :juego="juegoEditando" @submit="handleSubmit" />
        </AppModal>
    </div>
</template>

<style scoped>
.mis-juegos-view {
    max-width: 900px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
}

.encabezado {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: var(--space-4);
    margin-bottom: var(--space-6);
}

.encabezado h1 {
    margin: 0;
}

.estadisticas {
    display: flex;
    gap: var(--space-4);
    margin-bottom: var(--space-6);
    flex-wrap: wrap;
}

.stat-card {
    background: var(--color-footer-bg);
    border-radius: var(--radius-md);
    padding: var(--space-4);
    text-align: center;
    min-width: 120px;
    flex: 1;
}

.stat-numero {
    font-size: var(--font-size-2xl);
    font-weight: bold;
    color: var(--color-header-bg);
    margin: 0;
}

.stat-label {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin: var(--space-1) 0 0;
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

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-2);
}

.card-top h3 {
    margin: 0;
}

.favorito-btn {
    background: transparent;
    border: none;
    color: var(--color-text-secondary);
    cursor: pointer;
    padding: 0;
    display: flex;
    align-items: center;
    transition: transform 0.15s ease, color 0.15s ease;
    flex-shrink: 0;
}

.favorito-btn:hover {
    transform: scale(1.15);
}

.favorito-btn.activo {
    color: #ff6b6b;
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
    display: flex;
    align-items: center;
    gap: var(--space-1);
}

.acciones {
    display: flex;
    gap: var(--space-2);
    margin-top: var(--space-4);
}

.icon-btn {
    background: transparent;
    border: 1px solid var(--color-text-secondary);
    color: var(--color-text);
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-sm);
    cursor: pointer;
    display: flex;
    align-items: center;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.icon-btn:hover {
    transform: translateY(-1px);
}

.icon-btn-danger {
    border-color: #ff6b6b;
    color: #ff6b6b;
}

.app-button {
    display: inline-flex;
    align-items: center;
    gap: var(--space-1);
}

.error-modal {
    color: #ff6b6b;
    margin-bottom: var(--space-4);
}
</style>