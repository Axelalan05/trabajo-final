<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import { juegoService } from '@/services/juegoService'
import { userJuegoService } from '@/services/userJuegoService'
import { useAuthStore } from '@/stores/auth'
import type { Juego } from '@/types'
import { onMounted, ref } from 'vue'

const authStore = useAuthStore()

const juegos = ref<Juego[]>([])
const misJuegoIds = ref<Set<number>>(new Set())
const loading = ref(true)
const nombre = ref('')
const genero = ref('')
const plataforma = ref('')
const ordering = ref('-created_at')
const mensajeUnion = ref<{ id: number; texto: string } | null>(null)

const juegoDetalle = ref<Juego | null>(null)

async function cargarJuegos() {
    loading.value = true
    try {
        const response = await juegoService.listCatalogo({
            nombre: nombre.value || undefined,
            genero: genero.value || undefined,
            plataforma: plataforma.value || undefined,
            ordering: ordering.value,
        })
        juegos.value = response.data
    } finally {
        loading.value = false
    }
}

async function cargarMisJuegoIds() {
    if (!authStore.isAuthenticated) return
    const response = await userJuegoService.listMios()
    misJuegoIds.value = new Set(response.data.map((uj) => uj.juego.id))
}

async function unirseAJuego(juego: Juego) {
    mensajeUnion.value = null
    try {
        await userJuegoService.unirse({ juego_id: juego.id })
        misJuegoIds.value.add(juego.id)
    } catch (err: any) {
        const detail = err?.response?.data?.error?.details
        const mensaje = detail && typeof detail === 'object'
            ? (Object.values(detail).flat() as string[]).join(' ')
            : 'No se pudo unir al juego.'
        mensajeUnion.value = { id: juego.id, texto: mensaje }
    }
}

function truncar(texto: string, limite = 30): string {
    if (texto.length <= limite) return texto
    return texto.slice(0, limite).trimEnd() + '...'
}

function verDetalle(juego: Juego) {
    juegoDetalle.value = juego
}

onMounted(async () => {
    await cargarJuegos()
    await cargarMisJuegoIds()
})
</script>

<template>
    <div class="explorar-view">
        <h1>Explorar juegos</h1>

        <div class="filtros">
            <input v-model="nombre" placeholder="Nombre" @keyup.enter="cargarJuegos" />
            <input v-model="genero" placeholder="Género" @keyup.enter="cargarJuegos" />
            <input v-model="plataforma" placeholder="Plataforma" @keyup.enter="cargarJuegos" />
            <select v-model="ordering">
                <option value="-created_at">Más recientes</option>
                <option value="nombre">Nombre (A-Z)</option>
            </select>
            <AppButton @click="cargarJuegos">Filtrar</AppButton>
        </div>

        <div v-if="loading">Cargando...</div>

        <div v-else-if="juegos.length === 0" class="vacio">
            No se encontraron juegos.
        </div>

        <div v-else class="lista-juegos">
            <div v-for="juego in juegos" :key="juego.id" class="juego-card" @click="verDetalle(juego)">
                <img v-if="juego.imagen_url" :src="juego.imagen_url" :alt="juego.nombre" class="portada" />
                <div class="juego-card-body">
                    <h3>{{ juego.nombre }}</h3>
                    <p class="detalle">
                        {{ juego.genero }} · {{ juego.plataforma }}
                        <span v-if="juego.fecha_lanzamiento"> · {{ juego.fecha_lanzamiento.slice(0, 4) }}</span>
                    </p>
                    <p v-if="juego.descripcion" class="descripcion">{{ truncar(juego.descripcion) }}</p>

                    <p v-if="mensajeUnion?.id === juego.id" class="error-union">{{ mensajeUnion.texto }}</p>

                    <AppButton v-if="authStore.isAuthenticated && !misJuegoIds.has(juego.id)"
                        @click.stop="unirseAJuego(juego)">
                        Unirme
                    </AppButton>
                    <p v-else-if="authStore.isAuthenticated" class="ya-unido">Ya está en tu colección</p>
                </div>
            </div>
        </div>

        <AppModal :show="!!juegoDetalle" :title="juegoDetalle?.nombre ?? ''" @close="juegoDetalle = null">
            <img v-if="juegoDetalle?.imagen_url" :src="juegoDetalle.imagen_url" :alt="juegoDetalle.nombre"
                class="detalle-portada" />
            <p class="detalle-meta">
                {{ juegoDetalle?.genero }} · {{ juegoDetalle?.plataforma }}
                <span v-if="juegoDetalle?.fecha_lanzamiento"> · {{ juegoDetalle.fecha_lanzamiento.slice(0, 4) }}</span>
            </p>
            <p class="detalle-descripcion">{{ juegoDetalle?.descripcion || 'Sin descripción.' }}</p>
        </AppModal>
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
    overflow: hidden;
    text-align: left;
    cursor: pointer;
    transition: transform 0.15s ease;
}

.juego-card:hover {
    transform: translateY(-2px);
}

.portada {
    width: 100%;
    height: 140px;
    object-fit: cover;
    display: block;
}

.juego-card-body {
    padding: var(--space-4);
}

.detalle {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
}

.descripcion {
    margin-top: var(--space-2);
    font-size: var(--font-size-sm);
}

.ya-unido {
    margin-top: var(--space-3);
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    font-style: italic;
}

.error-union {
    color: #ff6b6b;
    font-size: var(--font-size-sm);
    margin-top: var(--space-2);
}

.detalle-portada {
    width: 100%;
    height: 220px;
    object-fit: cover;
    border-radius: var(--radius-md);
    margin-bottom: var(--space-4);
}

.detalle-meta {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin-bottom: var(--space-3);
}

.detalle-descripcion {
    white-space: pre-line;
    line-height: 1.5;
}
</style>