<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue';
import AppModal from '@/components/ui/AppModal.vue';
import AppPagination from '@/components/ui/AppPagination.vue';
import AppSpinner from '@/components/ui/AppSpinner.vue';
import { juegoService } from '@/services/juegoService';
import { userJuegoService } from '@/services/userJuegoService';
import { useAuthStore } from '@/stores/auth';
import { useToast } from '@/stores/toast';
import type { Juego } from '@/types';
import { Eye } from 'lucide-vue-next';
import { computed, onMounted, ref, watch } from 'vue';

const authStore = useAuthStore()
const { addToast } = useToast()

const JUEGOS_POR_PAGINA = 15

const juegos = ref<Juego[]>([])
const misJuegoIds = ref<Set<number>>(new Set())
const loading = ref(true)
const nombre = ref('')
const genero = ref('')
const plataforma = ref('')
const ordering = ref('-created_at')
const mensajeUnion = ref<{ id: number; texto: string } | null>(null)
const paginaActual = ref(1)

let searchTimer: ReturnType<typeof setTimeout>
watch([nombre, genero, plataforma], () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    cargarJuegos()
  }, 350)
})

const juegoDetalle = ref<Juego | null>(null)
const descripcionExpandida = ref(false)

const MAX_DESCRIPCION = 500

const descripcionModal = computed(() => {
    const texto = juegoDetalle.value?.descripcion
    if (!texto) return 'Sin descripción.'
    if (descripcionExpandida.value) return texto
    if (texto.length <= MAX_DESCRIPCION) return texto
    return texto.slice(0, MAX_DESCRIPCION).trimEnd() + '...'
})

const descripcionExcedeLimite = computed(() => {
    return (juegoDetalle.value?.descripcion?.length ?? 0) > MAX_DESCRIPCION
})

const totalPaginas = computed(() =>
    Math.max(1, Math.ceil(juegos.value.length / JUEGOS_POR_PAGINA))
)

const juegosPagina = computed(() => {
    const inicio = (paginaActual.value - 1) * JUEGOS_POR_PAGINA
    return juegos.value.slice(inicio, inicio + JUEGOS_POR_PAGINA)
})

function cambiarPagina(pagina: number) {
    paginaActual.value = pagina
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function cargarJuegos() {
    loading.value = true
    try {
        const response = await juegoService.listPublico({
            nombre: nombre.value || undefined,
            genero: genero.value || undefined,
            plataforma: plataforma.value || undefined,
            ordering: ordering.value,
        })
        juegos.value = response.data
        paginaActual.value = 1
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
        addToast(`Te uniste a "${juego.nombre}"`, 'success', 'userPlus')
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
    descripcionExpandida.value = false
    juegoDetalle.value = juego
}

function toggleDescripcion() {
    descripcionExpandida.value = !descripcionExpandida.value
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

        <AppSpinner v-if="loading" />

        <div v-else-if="juegos.length === 0" class="vacio">
            No se encontraron juegos.
        </div>

        <template v-else>
            <div class="lista-juegos">
                <div v-for="juego in juegosPagina" :key="juego.id" class="juego-card" @click="verDetalle(juego)">
                    <img v-if="juego.imagen_url" :src="juego.imagen_url" :alt="juego.nombre" class="portada" />
                    <div class="juego-card-body">
                        <h3>{{ juego.nombre }}</h3>
                        <p class="detalle">
                            {{ juego.genero }} · {{ juego.plataforma }}
                            <span v-if="juego.fecha_lanzamiento"> · {{ juego.fecha_lanzamiento.slice(0, 4) }}</span>
                        </p>
                        <p v-if="juego.descripcion" class="descripcion">{{ truncar(juego.descripcion) }}</p>

                        <p v-if="mensajeUnion?.id === juego.id" class="error-union">{{ mensajeUnion.texto }}</p>

                        <div class="card-acciones">
                            <AppButton v-if="authStore.isAuthenticated && !misJuegoIds.has(juego.id)"
                                @click.stop="unirseAJuego(juego)">
                                Unirme
                            </AppButton>
                            <p v-else-if="authStore.isAuthenticated" class="ya-unido">Ya está en tu colección</p>
                            <p v-else class="login-msg">
                                <router-link to="/login" @click.stop>Inicia sesión</router-link>
                                para unirte a este juego
                            </p>

                            <router-link :to="`/juegos/${juego.id}`" class="btn-ojo" @click.stop>
                                <Eye :size="18" />
                            </router-link>
                        </div>

                    </div>
                </div>
            </div>

            <AppPagination :pagina-actual="paginaActual" :total-paginas="totalPaginas"
                @update:pagina-actual="cambiarPagina" />
        </template>

        <AppModal :show="!!juegoDetalle" :title="juegoDetalle?.nombre ?? ''" @close="juegoDetalle = null">
            <img v-if="juegoDetalle?.imagen_url" :src="juegoDetalle.imagen_url" :alt="juegoDetalle.nombre"
                class="detalle-portada" />
            <p class="detalle-meta">
                {{ juegoDetalle?.genero }} · {{ juegoDetalle?.plataforma }}
                <span v-if="juegoDetalle?.fecha_lanzamiento"> · {{ juegoDetalle.fecha_lanzamiento.slice(0, 4) }}</span>
            </p>
            <p class="detalle-descripcion">{{ descripcionModal }}</p>
            <button v-if="descripcionExcedeLimite" class="toggle-descripcion" @click="toggleDescripcion">
                {{ descripcionExpandida ? 'Ver menos' : 'Ver más' }}
            </button>
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
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    animation: fadeSlideUp 0.4s ease both;
}

.juego-card:nth-child(1) { animation-delay: 0.02s; }
.juego-card:nth-child(2) { animation-delay: 0.04s; }
.juego-card:nth-child(3) { animation-delay: 0.06s; }
.juego-card:nth-child(4) { animation-delay: 0.08s; }
.juego-card:nth-child(5) { animation-delay: 0.10s; }
.juego-card:nth-child(6) { animation-delay: 0.12s; }
.juego-card:nth-child(7) { animation-delay: 0.14s; }
.juego-card:nth-child(8) { animation-delay: 0.16s; }
.juego-card:nth-child(9) { animation-delay: 0.18s; }
.juego-card:nth-child(10) { animation-delay: 0.20s; }

.juego-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.35);
}

@keyframes fadeSlideUp {
    from {
        opacity: 0;
        transform: translateY(15px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
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

.card-acciones {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    margin-top: var(--space-3);
}

.btn-ojo {
    background: transparent;
    border: 1px solid var(--color-text-secondary);
    color: var(--color-text);
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-sm);
    cursor: pointer;
    display: flex;
    align-items: center;
    text-decoration: none;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.btn-ojo:hover {
    transform: translateY(-1px);
    border-color: var(--color-header-bg);
    color: var(--color-header-bg);
}

.login-msg {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    margin: 0;
}

.login-msg a {
    color: var(--color-header-bg);
    text-decoration: underline;
    font-weight: 600;
}

.toggle-descripcion {
    background: transparent;
    border: none;
    color: var(--color-header-bg);
    cursor: pointer;
    font-weight: 600;
    font-size: var(--font-size-sm);
    padding: 0;
    margin-top: var(--space-2);
    text-decoration: underline;
}

.toggle-descripcion:hover {
    opacity: 0.8;
}
</style>