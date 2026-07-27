<script setup lang="ts">
import JuegoForm from '@/components/juegos/JuegoForm.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import AppSpinner from '@/components/ui/AppSpinner.vue'
import { juegoService } from '@/services/juegoService'
import { useToast } from '@/stores/toast'
import type { Juego, RawgResultado } from '@/types'
import { Pencil, Plus, Search, Trash2 } from 'lucide-vue-next'
import { computed, onMounted, ref, watch } from 'vue'

const { addToast } = useToast()

const JUEGOS_POR_PAGINA = 15

const juegos = ref<Juego[]>([])
const loading = ref(true)
const paginaActual = ref(1)
const nombre = ref('')
const genero = ref('')
const plataforma = ref('')
const ordering = ref('-created_at')

let searchTimer: ReturnType<typeof setTimeout>
watch([nombre, genero, plataforma], () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    cargarJuegos()
  }, 350)
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

// Modal 1: buscar en RAWG
const showBuscarModal = ref(false)
const queryBusqueda = ref('')
const resultadosBusqueda = ref<RawgResultado[]>([])
const buscando = ref(false)
const errorBusqueda = ref('')

// Modal 2: formulario de creación/edición
const showFormModal = ref(false)
const juegoEditando = ref<Partial<Juego> | null>(null)
const errorSubmit = ref('')

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
        paginaActual.value = 1
    } finally {
        loading.value = false
    }
}

function abrirBuscarModal() {
    queryBusqueda.value = ''
    resultadosBusqueda.value = []
    errorBusqueda.value = ''
    showBuscarModal.value = true
}

function cerrarBuscarModal() {
    showBuscarModal.value = false
}

async function buscarEnRawg() {
    if (!queryBusqueda.value.trim()) return
    buscando.value = true
    errorBusqueda.value = ''
    try {
        const response = await juegoService.rawgBuscar(queryBusqueda.value.trim())
        resultadosBusqueda.value = response.data
    } catch {
        errorBusqueda.value = 'No se pudo buscar en RAWG. Probá de nuevo.'
    } finally {
        buscando.value = false
    }
}

async function elegirResultado(resultado: RawgResultado) {
    buscando.value = true
    try {
        const detalle = await juegoService.rawgDetalle(resultado.rawg_id)
        juegoEditando.value = detalle.data
        showBuscarModal.value = false
        errorSubmit.value = ''
        showFormModal.value = true
    } catch {
        errorBusqueda.value = 'No se pudo traer el detalle de ese juego.'
    } finally {
        buscando.value = false
    }
}

function abrirModalEditar(juego: Juego) {
    juegoEditando.value = juego
    errorSubmit.value = ''
    showFormModal.value = true
}

function cerrarFormModal() {
    showFormModal.value = false
    juegoEditando.value = null
    errorSubmit.value = ''
}

async function handleSubmit(data: Partial<Juego>) {
    errorSubmit.value = ''
    try {
        if (juegoEditando.value?.id) {
            await juegoService.update(juegoEditando.value.id, data)
            addToast(`Juego "${data.nombre}" actualizado`, 'success', 'pencil')
        } else {
            await juegoService.create(data)
            addToast(`Juego "${data.nombre}" agregado al catálogo`, 'success', 'plus')
        }
        cerrarFormModal()
        await cargarJuegos()
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
    if (!confirm('¿Seguro que querés eliminar este juego del catálogo?')) return
    const juego = juegos.value.find((j) => j.id === id)
    await juegoService.delete(id)
    juegos.value = juegos.value.filter((j) => j.id !== id)
    if (juego) addToast(`Juego "${juego.nombre}" eliminado`, 'error', 'trash2')
}

onMounted(cargarJuegos)
</script>

<template>
    <div class="admin-juegos-view">
        <div class="encabezado">
            <h1>Administrar catálogo</h1>
            <AppButton @click="abrirBuscarModal">
                <Plus :size="18" /> Agregar juego
            </AppButton>
        </div>

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
            Todavía no hay juegos en el catálogo.
        </div>

        <template v-else>
            <div class="lista-juegos">
                <div v-for="juego in juegosPagina" :key="juego.id" class="juego-card">
                    <img v-if="juego.imagen_url" :src="juego.imagen_url" :alt="juego.nombre" class="portada" />
                    <div class="juego-card-body">
                        <h3>{{ juego.nombre }}</h3>
                        <p class="detalle">{{ juego.genero }} · {{ juego.plataforma }}</p>
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
            </div>

            <AppPagination :pagina-actual="paginaActual" :total-paginas="totalPaginas"
                @update:pagina-actual="cambiarPagina" />
        </template>

        <!-- Modal 1: buscar en RAWG -->
        <AppModal :show="showBuscarModal" title="Buscar en RAWG" @close="cerrarBuscarModal">
            <div class="buscador">
                <input v-model="queryBusqueda" type="text" placeholder="Nombre del juego..."
                    @keyup.enter="buscarEnRawg" />
                <AppButton @click="buscarEnRawg">
                    <Search :size="18" /> Buscar
                </AppButton>
            </div>

            <p v-if="errorBusqueda" class="error-modal">{{ errorBusqueda }}</p>
            <p v-if="buscando">Buscando...</p>

            <div v-if="resultadosBusqueda.length > 0" class="resultados-rawg">
                <button v-for="resultado in resultadosBusqueda" :key="resultado.rawg_id" class="resultado-card"
                    @click="elegirResultado(resultado)">
                    <img v-if="resultado.imagen_url" :src="resultado.imagen_url" :alt="resultado.nombre"
                        class="resultado-portada" />
                    <div class="resultado-info">
                        <p class="resultado-nombre">{{ resultado.nombre }}</p>
                        <p class="resultado-detalle">{{ resultado.fecha_lanzamiento?.slice(0, 4) ?? '—' }} · {{
                            resultado.plataforma }}</p>
                    </div>
                </button>
            </div>
        </AppModal>

        <!-- Modal 2: confirmar/editar datos antes de guardar -->
        <AppModal :show="showFormModal" :title="juegoEditando?.id ? 'Editar juego' : 'Confirmar datos del juego'"
            @close="cerrarFormModal">
            <p v-if="errorSubmit" class="error-modal">{{ errorSubmit }}</p>
            <JuegoForm :juego="juegoEditando" @submit="handleSubmit" />
        </AppModal>
    </div>
</template>

<style scoped>
.admin-juegos-view {
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

.error-modal {
    color: #ff6b6b;
    margin-bottom: var(--space-4);
}

.buscador {
    display: flex;
    gap: var(--space-2);
    margin-bottom: var(--space-4);
}

.buscador input {
    flex: 1;
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
}

.resultados-rawg {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
    max-height: 400px;
    overflow-y: auto;
}

.resultado-card {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    background: var(--color-footer-bg);
    border: none;
    border-radius: var(--radius-sm);
    padding: var(--space-2);
    cursor: pointer;
    text-align: left;
    color: var(--color-text);
    transition: transform 0.15s ease;
}

.resultado-card:hover {
    transform: translateY(-1px);
}

.resultado-portada {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.resultado-nombre {
    font-weight: bold;
    margin: 0;
}

.resultado-detalle {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin: var(--space-1) 0 0;
}
</style>
