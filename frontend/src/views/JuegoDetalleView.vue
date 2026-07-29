<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import AppSpinner from '@/components/ui/AppSpinner.vue'
import { juegoService, type Jugador } from '@/services/juegoService'
import { userJuegoService } from '@/services/userJuegoService'
import { useAuthStore } from '@/stores/auth'
import { useToast } from '@/stores/toast'
import type { EstadoJuego, JuegoDetalleResponse } from '@/types'
import { ArrowLeft, Eye, Search } from 'lucide-vue-next'
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const { addToast } = useToast()

const loading = ref(true)
const detalle = ref<JuegoDetalleResponse | null>(null)
const error = ref('')

// Estado local para editar mi_user_juego
const miEstado = ref<EstadoJuego>('pendiente')
const miPuntaje = ref<number | null>(null)
const miResenia = ref('')
const saving = ref(false)
const mensaje = ref('')

// Jugadores que tienen este juego en su colección (búsqueda en vivo + paginación)
const jugadores = ref<Jugador[]>([])
const loadingJugadores = ref(true)
const busquedaJugadores = ref('')
const paginaJugadores = ref(1)
const totalPaginasJugadores = ref(1)
const totalJugadores = ref(0)

const ESTADO_LABELS: Record<EstadoJuego, string> = {
    pendiente: 'Pendiente',
    jugando: 'Jugando',
    completado: 'Completado',
    abandonado: 'Abandonado',
}

async function cargarDetalle() {
    loading.value = true
    error.value = ''
    try {
        const juegoId = Number(route.params.id)
        const response = await juegoService.getDetalle(juegoId)
        detalle.value = response.data

        // Si el usuario ya tiene este juego, precargamos sus datos
        if (response.data.mi_user_juego) {
            miEstado.value = response.data.mi_user_juego.estado
            miPuntaje.value = response.data.mi_user_juego.puntaje
            miResenia.value = response.data.mi_user_juego.resenia
        }
    } catch {
        error.value = 'No se pudo cargar el detalle del juego.'
    } finally {
        loading.value = false
    }
}

async function cargarJugadores() {
    loadingJugadores.value = true
    try {
        const juegoId = Number(route.params.id)
        const response = await juegoService.listJugadores(juegoId, {
            q: busquedaJugadores.value || undefined,
            page: paginaJugadores.value,
        })
        jugadores.value = response.jugadores
        totalPaginasJugadores.value = response.total_pages
        totalJugadores.value = response.total
    } catch {
        jugadores.value = []
    } finally {
        loadingJugadores.value = false
    }
}

let searchTimer: ReturnType<typeof setTimeout>
watch(busquedaJugadores, () => {
    clearTimeout(searchTimer)
    searchTimer = setTimeout(() => {
        paginaJugadores.value = 1
        cargarJugadores()
    }, 350)
})

function cambiarPaginaJugadores(pagina: number) {
    paginaJugadores.value = pagina
    cargarJugadores()
}

function volver() {
    router.back()
}

async function unirseAlJuego() {
    if (!detalle.value || !authStore.isAuthenticated) return
    saving.value = true
    mensaje.value = ''
    try {
        const response = await userJuegoService.unirse({
            juego_id: detalle.value.juego.id,
            estado: miEstado.value,
            puntaje: miPuntaje.value,
            resenia: miResenia.value,
        })
        detalle.value.mi_user_juego = response.data
        mensaje.value = 'Juego agregado a tu colección ✅'
        addToast(`"${detalle.value.juego.nombre}" agregado a tu colección`, 'success', 'userPlus')
        cargarJugadores()
    } catch (err: any) {
        const detail = err?.response?.data?.error?.details
        mensaje.value = detail && typeof detail === 'object'
            ? (Object.values(detail).flat() as string[]).join(' ')
            : 'Error al agregar el juego.'
    } finally {
        saving.value = false
    }
}

async function actualizarMiJuego() {
    if (!detalle.value?.mi_user_juego) return
    saving.value = true
    mensaje.value = ''
    try {
        const response = await userJuegoService.actualizar(detalle.value.mi_user_juego.id, {
            estado: miEstado.value,
            puntaje: miPuntaje.value,
            resenia: miResenia.value,
        })
        detalle.value.mi_user_juego = response.data
        mensaje.value = 'Actualizado ✅'
        addToast(`Progreso actualizado para "${detalle.value.juego.nombre}"`, 'success', 'pencil')
        cargarJugadores()
    } catch {
        mensaje.value = 'Error al actualizar.'
    } finally {
        saving.value = false
    }
}

function renderEstrellas(puntaje: number | null): string {
    if (!puntaje) return '—'
    const llenas = Math.round(puntaje / 2) // Convertimos 1-10 a 0.5-5 estrellas
    return '★'.repeat(llenas) + '☆'.repeat(5 - llenas)
}

onMounted(() => {
    cargarDetalle()
    cargarJugadores()
})
</script>

<template>
    <div class="detalle-view">
        <AppSpinner v-if="loading" />

        <div v-else-if="error" class="error">
            <p>{{ error }}</p>
            <AppButton @click="volver">Volver</AppButton>
        </div>

        <template v-else-if="detalle">
            <!-- Botón volver -->
            <button class="btn-volver" @click="volver">
                <ArrowLeft :size="20" /> Volver
            </button>

            <!-- Hero con portada -->
            <div class="hero">
                <img v-if="detalle.juego.imagen_url" :src="detalle.juego.imagen_url" :alt="detalle.juego.nombre"
                    class="portada-hero" />
                <div class="hero-info">
                    <h1>{{ detalle.juego.nombre }}</h1>
                    <p class="meta">
                        {{ detalle.juego.genero }} · {{ detalle.juego.plataforma }}
                        <span v-if="detalle.juego.fecha_lanzamiento">
                            · {{ detalle.juego.fecha_lanzamiento }}
                        </span>
                    </p>

                    <!-- Puntaje promedio con estrellas -->
                    <div class="puntaje-promedio" v-if="detalle.puntaje_promedio">
                        <span class="estrellas">{{ renderEstrellas(detalle.puntaje_promedio) }}</span>
                        <span class="promedio-numero">{{ detalle.puntaje_promedio }}/10</span>
                        <span class="total-resenias">({{ detalle.total_resenias }} reseñas)</span>
                    </div>
                    <p v-else class="sin-resenias">Sin reseñas todavía</p>
                </div>
            </div>

            <!-- Descripción -->
            <section class="seccion">
                <h2>Descripción</h2>
                <p class="descripcion">{{ detalle.juego.descripcion || 'Sin descripción disponible.' }}</p>
            </section>

            <!-- Sección para el usuario autenticado -->
            <section v-if="authStore.isAuthenticated" class="seccion seccion-usuario">
                <h2>{{ detalle.mi_user_juego ? 'Mi progreso' : 'Agregar a mi colección' }}</h2>

                <div class="formulario">
                    <div class="campo">
                        <label for="estado">Estado</label>
                        <select id="estado" v-model="miEstado">
                            <option value="pendiente">Pendiente</option>
                            <option value="jugando">Jugando</option>
                            <option value="completado">Completado</option>
                            <option value="abandonado">Abandonado</option>
                        </select>
                    </div>

                    <div class="campo">
                        <label for="puntaje">Puntaje (1-10)</label>
                        <input id="puntaje" type="number" min="1" max="10" v-model.number="miPuntaje"
                            placeholder="Opcional" />
                    </div>

                    <div class="campo">
                        <label for="resenia">Reseña</label>
                        <textarea id="resenia" v-model="miResenia" rows="4"
                            placeholder="Escribí tu reseña..."></textarea>
                    </div>

                    <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>

                    <AppButton v-if="detalle.mi_user_juego" @click="actualizarMiJuego" :disabled="saving">
                        {{ saving ? 'Guardando...' : 'Guardar cambios' }}
                    </AppButton>
                    <AppButton v-else @click="unirseAlJuego" :disabled="saving">
                        {{ saving ? 'Agregando...' : 'Agregar a mi colección' }}
                    </AppButton>
                </div>
            </section>

            <!-- Si no está autenticado -->
            <section v-else class="seccion">
                <p class="login-cta">
                    <router-link to="/login">Iniciá sesión</router-link> para agregar este juego a tu colección.
                </p>
            </section>

            <!-- Quiénes lo tienen en su colección -->
            <section class="seccion">
                <h2>Jugadores ({{ totalJugadores }})</h2>

                <div class="buscador-jugadores">
                    <Search :size="16" class="icono-buscar" />
                    <input v-model="busquedaJugadores" type="text" placeholder="Buscar por nombre de usuario..." />
                </div>

                <AppSpinner v-if="loadingJugadores" />

                <div v-else-if="jugadores.length === 0" class="vacio-jugadores">
                    <span v-if="busquedaJugadores">No hay usuarios que coincidan con "{{ busquedaJugadores }}".</span>
                    <span v-else>Todavía nadie agregó este juego a su colección.</span>
                </div>

                <template v-else>
                    <ul class="lista-jugadores">
                        <li v-for="jugador in jugadores" :key="jugador.username" class="jugador-item">
                            <span class="jugador-username">{{ jugador.username }}</span>
                            <span class="jugador-estado" :class="`estado-${jugador.estado}`">
                                {{ ESTADO_LABELS[jugador.estado] }}
                            </span>
                            <span class="jugador-puntaje">{{ jugador.puntaje ? `${jugador.puntaje}/10` : '—' }}</span>
                            <router-link :to="`/usuarios/${jugador.username}`" class="btn-ojo"
                                aria-label="Ver perfil público">
                                <Eye :size="18" />
                            </router-link>
                        </li>
                    </ul>

                    <AppPagination :pagina-actual="paginaJugadores" :total-paginas="totalPaginasJugadores"
                        @update:pagina-actual="cambiarPaginaJugadores" />
                </template>
            </section>
        </template>
    </div>
</template>

<style scoped>
.detalle-view {
    max-width: 800px;
    margin: var(--space-6) auto;
    padding: var(--space-6);
    color: var(--color-text);
}

.btn-volver {
    background: transparent;
    border: 1px solid var(--color-text-secondary);
    color: var(--color-text);
    padding: var(--space-2) var(--space-3);
    border-radius: var(--radius-md);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: var(--space-2);
    font-family: var(--font-sans);
    font-size: var(--font-size-sm);
    transition: transform 0.15s ease, border-color 0.15s ease;
    margin-bottom: var(--space-6);
}

.btn-volver:hover {
    transform: translateY(-1px);
    border-color: var(--color-header-bg);
}

.hero {
    display: flex;
    gap: var(--space-6);
    margin-bottom: var(--space-8);
    flex-wrap: wrap;
}

.portada-hero {
    width: 300px;
    max-width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: var(--radius-md);
    flex-shrink: 0;
}

.hero-info {
    flex: 1;
    min-width: 200px;
}

.hero-info h1 {
    margin: 0 0 var(--space-2);
    font-size: var(--font-size-2xl);
}

.meta {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin-bottom: var(--space-4);
}

.puntaje-promedio {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    flex-wrap: wrap;
}

.estrellas {
    font-size: var(--font-size-xl);
    color: #ffd93d;
    letter-spacing: 2px;
}

.promedio-numero {
    font-weight: bold;
    font-size: var(--font-size-lg);
}

.total-resenias {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
}

.sin-resenias {
    color: var(--color-text-secondary);
    font-style: italic;
}

.seccion {
    background: var(--color-footer-bg);
    border-radius: var(--radius-md);
    padding: var(--space-6);
    margin-bottom: var(--space-6);
}

.seccion h2 {
    margin: 0 0 var(--space-4);
}

.descripcion {
    line-height: 1.7;
    white-space: pre-line;
    color: var(--color-text-secondary);
}

.seccion-usuario {
    border: 1px solid var(--color-header-bg);
}

.formulario {
    display: flex;
    flex-direction: column;
    gap: var(--space-4);
}

.campo {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
}

.campo label {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    font-weight: 500;
}

.campo select,
.campo input,
.campo textarea {
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
    font-family: var(--font-sans);
    font-size: var(--font-size-base);
    background: var(--color-bg);
    color: var(--color-text);
}

.campo textarea {
    resize: vertical;
    min-height: 80px;
}

.mensaje {
    color: var(--color-header-bg);
    font-weight: 500;
}

.login-cta {
    text-align: center;
    color: var(--color-text-secondary);
}

.login-cta a {
    color: var(--color-header-bg);
    font-weight: bold;
}

.error {
    text-align: center;
    color: #ff6b6b;
    padding: var(--space-8);
}

.buscador-jugadores {
    position: relative;
    margin-bottom: var(--space-4);
}

.icono-buscar {
    position: absolute;
    left: var(--space-3);
    top: 50%;
    transform: translateY(-50%);
    color: var(--color-text-secondary);
    pointer-events: none;
}

.buscador-jugadores input {
    width: 100%;
    padding: var(--space-2) var(--space-2) var(--space-2) calc(var(--space-3) * 2 + 16px);
    border-radius: var(--radius-sm);
    border: none;
    font-family: var(--font-sans);
    font-size: var(--font-size-base);
    background: var(--color-bg);
    color: var(--color-text);
    box-sizing: border-box;
}

.vacio-jugadores {
    color: var(--color-text-secondary);
    text-align: center;
    padding: var(--space-4) 0;
}

.lista-jugadores {
    list-style: none;
    margin: 0 0 var(--space-4);
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
}

.jugador-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-2) var(--space-3);
    background: var(--color-bg);
    border-radius: var(--radius-sm);
}

.jugador-username {
    font-weight: 600;
    flex: 1;
    min-width: 0;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.jugador-estado {
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    white-space: nowrap;
}

.jugador-puntaje {
    font-size: var(--font-size-sm);
    font-weight: 600;
    color: var(--color-text-secondary);
    white-space: nowrap;
    min-width: 40px;
    text-align: right;
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
    flex-shrink: 0;
}

.btn-ojo:hover {
    transform: translateY(-1px);
    border-color: var(--color-header-bg);
    color: var(--color-header-bg);
}

@media (max-width: 600px) {
    .hero {
        flex-direction: column;
        align-items: center;
        text-align: center;
    }

    .portada-hero {
        width: 100%;
        height: 180px;
    }

    .puntaje-promedio {
        justify-content: center;
    }

    .jugador-item {
        flex-wrap: wrap;
    }

    .jugador-username {
        width: 100%;
    }
}
</style>