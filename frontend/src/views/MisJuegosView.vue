<script setup lang="ts">
import AppPagination from '@/components/ui/AppPagination.vue'
import AppSpinner from '@/components/ui/AppSpinner.vue'
import ConfirmModal from '@/components/ui/ConfirmModal.vue'
import { userJuegoService } from '@/services/userJuegoService'
import type { EstadoJuego, UserJuego } from '@/types'
import { Eye, Star, Trash2 } from 'lucide-vue-next'
import { computed, onMounted, ref } from 'vue'

const JUEGOS_POR_PAGINA = 15

const misJuegos = ref<UserJuego[]>([])
const loading = ref(true)
const paginaActual = ref(1)

const totalPaginas = computed(() =>
    Math.max(1, Math.ceil(misJuegos.value.length / JUEGOS_POR_PAGINA))
)

const misJuegosPagina = computed(() => {
    const inicio = (paginaActual.value - 1) * JUEGOS_POR_PAGINA
    return misJuegos.value.slice(inicio, inicio + JUEGOS_POR_PAGINA)
})

function cambiarPagina(pagina: number) {
    paginaActual.value = pagina
    window.scrollTo({ top: 0, behavior: 'smooth' })
}
const estadisticas = ref<{
    juegos_completados: number
    promedio_puntaje: number
    generos_mas_jugados: { juego__genero: string; total: number }[]
} | null>(null)

async function cargarMisJuegos() {
    loading.value = true
    try {
        const response = await userJuegoService.listMios()
        misJuegos.value = response.data
    } finally {
        loading.value = false
    }
}

async function cargarEstadisticas() {
    try {
        const response = await userJuegoService.estadisticas()
        estadisticas.value = response.data
    } catch {
        // silencioso
    }
}

async function actualizarEstado(userJuego: UserJuego, estado: EstadoJuego) {
    const response = await userJuegoService.actualizar(userJuego.id, { estado })
    userJuego.estado = response.data.estado
    await cargarEstadisticas()
}

async function actualizarPuntaje(userJuego: UserJuego, puntaje: number | null) {
    const response = await userJuegoService.actualizar(userJuego.id, { puntaje })
    userJuego.puntaje = response.data.puntaje
    await cargarEstadisticas()
}

function claseEstado(estado: EstadoJuego): string {
    return `estado-${estado}`
}

const juegoASalir = ref<UserJuego | null>(null)

function pedirSalir(userJuego: UserJuego) {
    juegoASalir.value = userJuego
}

async function confirmarSalir() {
    if (!juegoASalir.value) return
    const id = juegoASalir.value.id
    await userJuegoService.salir(id)
    misJuegos.value = misJuegos.value.filter((uj) => uj.id !== id)
    await cargarEstadisticas()
    juegoASalir.value = null
}

onMounted(async () => {
    await cargarMisJuegos()
    await cargarEstadisticas()
})
</script>

<template>
    <div class="mis-juegos-view">
        <div class="encabezado">
            <h1>Mi colección</h1>
        </div>

        <div v-if="estadisticas" class="estadisticas">
            <div class="stat-card">
                <p class="stat-numero">{{ misJuegos.length }}</p>
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
                <p class="stat-numero">{{ estadisticas.generos_mas_jugados[0]?.juego__genero ?? '—' }}</p>
                <p class="stat-label">Género favorito</p>
            </div>
        </div>

        <AppSpinner v-if="loading" />

        <div v-else-if="misJuegos.length === 0" class="vacio">
            Todavía no te uniste a ningún juego. Buscá algo en <router-link to="/explorar">Explorar</router-link>.
        </div>

        <template v-else>
            <div class="lista-juegos">
                <div v-for="userJuego in misJuegosPagina" :key="userJuego.id" class="juego-card">
                    <img v-if="userJuego.juego.imagen_url" :src="userJuego.juego.imagen_url"
                        :alt="userJuego.juego.nombre" class="portada" />
                    <div class="juego-card-body">
                        <div class="card-top">
                            <h3>{{ userJuego.juego.nombre }}</h3>
                            <div class="card-top-acciones">
                                <router-link :to="`/juegos/${userJuego.juego.id}`" class="icon-btn">
                                    <Eye :size="18" />
                                </router-link>
                                <button class="icon-btn icon-btn-danger" @click="pedirSalir(userJuego)">
                                    <Trash2 :size="18" />
                                </button>
                            </div>
                        </div>

                        <p class="detalle">
                            {{ userJuego.juego.genero }} · {{ userJuego.juego.plataforma }}
                        </p>

                        <div class="campo">
                            <label>Estado</label>
                            <select :class="claseEstado(userJuego.estado)" :value="userJuego.estado"
                                @change="actualizarEstado(userJuego, ($event.target as HTMLSelectElement).value as EstadoJuego)">
                                <option value="pendiente">Pendiente</option>
                                <option value="jugando">Jugando</option>
                                <option value="completado">Completado</option>
                                <option value="abandonado">Abandonado</option>
                            </select>
                        </div>

                        <div class="campo">
                            <label>Puntaje (1-10)</label>
                            <input type="number" min="1" max="10" :value="userJuego.puntaje"
                                @change="actualizarPuntaje(userJuego, ($event.target as HTMLInputElement).valueAsNumber || null)" />
                        </div>

                        <p v-if="userJuego.puntaje" class="puntaje">
                            <Star :size="16" /> {{ userJuego.puntaje }}/10
                        </p>
                    </div>
                </div>
            </div>

            <AppPagination :pagina-actual="paginaActual" :total-paginas="totalPaginas"
                @update:pagina-actual="cambiarPagina" />
        </template>
        <ConfirmModal :show="!!juegoASalir" title="Salir del juego"
            :mensaje="`¿Seguro que querés salir de '${juegoASalir?.juego.nombre}'? Perdés tu estado, puntaje y reseña de este juego.`"
            texto-confirmar="Salir" variant-confirmar="danger" @confirm="confirmarSalir" @close="juegoASalir = null" />
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
    overflow: hidden;
    text-align: left;
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

.card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: var(--space-2);
}

.card-top h3 {
    margin: 0;
}

.detalle {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin-bottom: var(--space-2);
}

.campo {
    margin-top: var(--space-2);
}

.campo label {
    display: block;
    margin-bottom: var(--space-1);
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
}

.campo input,
.campo select {
    width: 100%;
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
    font-family: var(--font-sans);
    box-sizing: border-box;
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

.estado-pendiente {
    color: #ffd93d !important;
    background: #3a3520 !important;
    border: 1px solid #ffd93d !important;
}

.estado-jugando {
    color: #6bcf7f !important;
    background: #1f3a24 !important;
    border: 1px solid #6bcf7f !important;
}

.estado-completado {
    color: #63d2ff !important;
    background: #1a3540 !important;
    border: 1px solid #63d2ff !important;
}

.estado-abandonado {
    color: #ff6b6b !important;
    background: #3a1f1f !important;
    border: 1px solid #ff6b6b !important;
}

.card-top-acciones {
    display: flex;
    gap: var(--space-2);
    align-items: center;
}

.vacio a {
    color: var(--color-header-bg);
    text-decoration: underline;
    font-weight: 600;
}

.vacio a:hover {
    color: var(--color-accent);
    opacity: 0.8;
}
</style>