<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import AppPagination from '@/components/ui/AppPagination.vue'
import AppSpinner from '@/components/ui/AppSpinner.vue'
import { userService, type AdminUser, type AdminUserDetail } from '@/services/userService'
import { Eye, Search, UserX } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'

const usuarios = ref<AdminUser[]>([])
const loading = ref(true)
const paginaActual = ref(1)
const totalPaginas = ref(1)
const totalUsuarios = ref(0)
const busqueda = ref('')
const error = ref('')

// Modal de detalle
const showDetailModal = ref(false)
const detalleUsuario = ref<AdminUserDetail | null>(null)
const loadingDetail = ref(false)

// Modal de confirmación para eliminar
const showDeleteConfirm = ref(false)
const usuarioAEliminar = ref<AdminUser | null>(null)
const deleting = ref(false)

async function cargarUsuarios() {
    loading.value = true
    error.value = ''
    try {
        const response = await userService.listUsers(busqueda.value, paginaActual.value)
        usuarios.value = response.users
        totalPaginas.value = response.total_pages
        totalUsuarios.value = response.total
    } catch (err: any) {
        error.value = err?.response?.data?.error?.message || 'Error al cargar usuarios.'
        usuarios.value = []
    } finally {
        loading.value = false
    }
}

function cambiarPagina(pagina: number) {
    paginaActual.value = pagina
    window.scrollTo({ top: 0, behavior: 'smooth' })
    cargarUsuarios()
}

function buscar() {
    paginaActual.value = 1
    cargarUsuarios()
}

async function verDetalle(userId: number) {
    loadingDetail.value = true
    showDetailModal.value = true
    try {
        const response = await userService.getUserDetail(userId)
        detalleUsuario.value = response.data
    } catch {
        detalleUsuario.value = null
    } finally {
        loadingDetail.value = false
    }
}

function cerrarDetalle() {
    showDetailModal.value = false
    detalleUsuario.value = null
}

function confirmarEliminar(usuario: AdminUser) {
    usuarioAEliminar.value = usuario
    showDeleteConfirm.value = true
}

function cancelarEliminar() {
    usuarioAEliminar.value = null
    showDeleteConfirm.value = false
}

async function eliminarUsuario() {
    if (!usuarioAEliminar.value) return
    deleting.value = true
    try {
        await userService.deleteUser(usuarioAEliminar.value.id)
        showDeleteConfirm.value = false
        usuarioAEliminar.value = null
        await cargarUsuarios()
    } catch (err: any) {
        error.value = err?.response?.data?.error?.message || 'Error al eliminar usuario.'
        showDeleteConfirm.value = false
        usuarioAEliminar.value = null
    } finally {
        deleting.value = false
    }
}

onMounted(cargarUsuarios)
</script>

<template>
    <div class="admin-usuarios-view">
        <div class="encabezado">
            <h1>Administrar usuarios</h1>
            <p class="total-usuarios" v-if="!loading">
                Total: <strong>{{ totalUsuarios }}</strong> usuario{{ totalUsuarios !== 1 ? 's' : '' }}
            </p>
        </div>

        <div class="barra-busqueda">
            <div class="input-wrapper">
                <Search :size="18" class="search-icon" />
                <input v-model="busqueda" placeholder="Buscar por nombre de usuario o correo..."
                    @keyup.enter="buscar" />
            </div>
            <AppButton @click="buscar">Buscar</AppButton>
        </div>

        <p v-if="error" class="error">{{ error }}</p>

        <AppSpinner v-if="loading" />

        <div v-else-if="usuarios.length === 0" class="vacio">
            No se encontraron usuarios.
        </div>

        <template v-else>
            <div class="tabla-container">
                <table class="tabla-usuarios">
                    <thead>
                        <tr>
                            <th>Nombre de usuario</th>
                            <th>Correo electrónico</th>
                            <th>Fecha de registro</th>
                            <th class="col-acciones">Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="usuario in usuarios" :key="usuario.id">
                            <td class="td-username">
                                <span class="admin-badge" v-if="usuario.is_staff">Admin</span>
                                {{ usuario.username }}
                            </td>
                            <td class="td-email">{{ usuario.email }}</td>
                            <td class="td-fecha">{{ new Date(usuario.date_joined).toLocaleDateString('es-AR') }}</td>
                            <td class="td-acciones">
                                <button class="icon-btn icon-btn-ver" @click="verDetalle(usuario.id)"
                                    title="Ver perfil y juegos">
                                    <Eye :size="18" />
                                </button>
                                <button class="icon-btn icon-btn-danger" @click="confirmarEliminar(usuario)"
                                    title="Expulsar usuario" :disabled="usuario.is_staff">
                                    <UserX :size="18" />
                                </button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <AppPagination :pagina-actual="paginaActual" :total-paginas="totalPaginas"
                @update:pagina-actual="cambiarPagina" />
        </template>

        <!-- Modal: Detalle del usuario -->
        <AppModal :show="showDetailModal" title="Detalle del usuario" @close="cerrarDetalle">
            <AppSpinner v-if="loadingDetail" />
            <div v-else-if="detalleUsuario" class="detalle-usuario">
                <div class="detalle-header">
                    <div class="detalle-avatar">
                        {{ detalleUsuario.username.charAt(0).toUpperCase() }}
                    </div>
                    <div class="detalle-info">
                        <h3>{{ detalleUsuario.username }}
                            <span class="admin-badge" v-if="detalleUsuario.is_staff">Admin</span>
                        </h3>
                        <p class="detalle-email">{{ detalleUsuario.email }}</p>
                        <p class="detalle-fecha">Registrado el {{ new
                            Date(detalleUsuario.date_joined).toLocaleDateString('es-AR') }}</p>
                    </div>
                </div>

                <h4 class="juegos-titulo">Juegos en los que se ha unido</h4>
                <div v-if="detalleUsuario.juegos.length === 0" class="sin-juegos">
                    Este usuario no se ha unido a ningún juego todavía.
                </div>
                <div v-else class="lista-juegos">
                    <div v-for="juego in detalleUsuario.juegos" :key="juego.juego_id" class="juego-item">
                        <img v-if="juego.juego_imagen" :src="juego.juego_imagen" :alt="juego.juego_nombre"
                            class="juego-portada" />
                        <div class="juego-info">
                            <p class="juego-nombre">{{ juego.juego_nombre }}</p>
                            <p class="juego-estado">
                                Estado: <span class="estado-badge">{{ juego.estado }}</span>
                            </p>
                            <p v-if="juego.puntaje" class="juego-puntaje">Puntaje: {{ juego.puntaje }}/10</p>
                            <p v-if="juego.resenia" class="juego-resenia">Reseña: {{ juego.resenia }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </AppModal>

        <!-- Modal: Confirmar eliminación -->
        <AppModal :show="showDeleteConfirm" title="Expulsar usuario" @close="cancelarEliminar">
            <div class="confirm-eliminar">
                <div class="confirm-icono">
                    <UserX :size="48" />
                </div>
                <p>
                    ¿Estás seguro de que querés <strong>expulsar</strong> al usuario
                    <strong>{{ usuarioAEliminar?.username }}</strong>?
                </p>
                <p class="confirm-aviso">Se eliminarán todos sus datos del sistema. Esta acción no se puede deshacer.
                </p>
                <div class="confirm-acciones">
                    <AppButton @click="cancelarEliminar" :disabled="deleting">Cancelar</AppButton>
                    <AppButton class="btn-eliminar" @click="eliminarUsuario" :disabled="deleting">
                        {{ deleting ? 'Eliminando...' : 'Sí, expulsar' }}
                    </AppButton>
                </div>
            </div>
        </AppModal>
    </div>
</template>

<style scoped>
.admin-usuarios-view {
    max-width: 1000px;
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

.total-usuarios {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin: 0;
}

.barra-busqueda {
    display: flex;
    gap: var(--space-2);
    margin-bottom: var(--space-6);
}

.input-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    background: var(--color-footer-bg);
    border-radius: var(--radius-sm);
    padding: 0 var(--space-3);
    border: 1px solid rgba(255, 255, 255, 0.15);
}

.search-icon {
    color: var(--color-text-secondary);
    flex-shrink: 0;
}

.input-wrapper input {
    flex: 1;
    padding: var(--space-2) var(--space-2);
    background: transparent;
    border: none;
    color: var(--color-text);
    font-family: var(--font-sans);
    outline: none;
}

.input-wrapper input::placeholder {
    color: var(--color-text-secondary);
}

.error {
    color: #ff6b6b;
    margin-bottom: var(--space-4);
}

.vacio {
    color: var(--color-text-secondary);
    text-align: center;
    margin-top: var(--space-8);
}

.tabla-container {
    overflow-x: auto;
}

.tabla-usuarios {
    width: 100%;
    border-collapse: collapse;
    background: var(--color-footer-bg);
    border-radius: var(--radius-md);
    overflow: hidden;
}

.tabla-usuarios th {
    text-align: left;
    padding: var(--space-3) var(--space-4);
    background: rgba(255, 255, 255, 0.06);
    color: var(--color-text-secondary);
    font-weight: 600;
    font-size: var(--font-size-sm);
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.tabla-usuarios td {
    padding: var(--space-3) var(--space-4);
    border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.tabla-usuarios tr:hover {
    background: rgba(255, 255, 255, 0.03);
}

.admin-badge {
    display: inline-block;
    background: var(--color-header-bg);
    color: var(--color-header-text);
    font-size: var(--font-size-xs);
    font-weight: bold;
    padding: 2px 6px;
    border-radius: var(--radius-full);
    margin-right: var(--space-1);
    vertical-align: middle;
}

.td-username {
    font-weight: 600;
}

.td-email {
    color: var(--color-text-secondary);
}

.td-fecha {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    white-space: nowrap;
}

.col-acciones {
    text-align: center;
    width: 100px;
}

.td-acciones {
    text-align: center;
    display: flex;
    gap: var(--space-2);
    justify-content: center;
}

.icon-btn {
    background: transparent;
    border: 1px solid var(--color-text-secondary);
    color: var(--color-text);
    padding: var(--space-1) var(--space-2);
    border-radius: var(--radius-sm);
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    transition: transform 0.15s ease, border-color 0.15s ease;
}

.icon-btn:hover {
    transform: translateY(-1px);
}

.icon-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
    transform: none;
}

.icon-btn-ver:hover {
    border-color: var(--color-header-bg);
    color: var(--color-header-bg);
}

.icon-btn-danger {
    border-color: #ff6b6b;
    color: #ff6b6b;
}

.icon-btn-danger:hover:not(:disabled) {
    background: rgba(255, 107, 107, 0.1);
}

/* Detalle del usuario en el modal */
.detalle-usuario {
    padding: var(--space-2) 0;
}

.detalle-header {
    display: flex;
    gap: var(--space-4);
    align-items: center;
    margin-bottom: var(--space-6);
    padding-bottom: var(--space-4);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.detalle-avatar {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--color-header-bg);
    color: var(--color-header-text);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    font-weight: bold;
    flex-shrink: 0;
}

.detalle-info h3 {
    margin: 0 0 var(--space-1);
}

.detalle-email {
    color: var(--color-text-secondary);
    margin: 0 0 var(--space-1);
    font-size: var(--font-size-sm);
}

.detalle-fecha {
    color: var(--color-text-secondary);
    margin: 0;
    font-size: var(--font-size-xs);
}

.juegos-titulo {
    margin: 0 0 var(--space-3);
    color: var(--color-text);
}

.sin-juegos {
    color: var(--color-text-secondary);
    text-align: center;
    padding: var(--space-6) 0;
}

.lista-juegos {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    max-height: 350px;
    overflow-y: auto;
}

.juego-item {
    display: flex;
    gap: var(--space-3);
    background: rgba(255, 255, 255, 0.03);
    border-radius: var(--radius-sm);
    padding: var(--space-3);
}

.juego-portada {
    width: 60px;
    height: 60px;
    object-fit: cover;
    border-radius: var(--radius-sm);
    flex-shrink: 0;
}

.juego-info {
    flex: 1;
    min-width: 0;
}

.juego-nombre {
    font-weight: bold;
    margin: 0 0 var(--space-1);
}

.juego-estado {
    margin: 0 0 var(--space-1);
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
}

.estado-badge {
    display: inline-block;
    background: rgba(104, 249, 159, 0.15);
    color: var(--color-header-bg);
    padding: 1px 8px;
    border-radius: var(--radius-full);
    font-size: var(--font-size-xs);
    font-weight: 600;
}

.juego-puntaje {
    margin: 0 0 var(--space-1);
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
}

.juego-resenia {
    margin: 0;
    font-size: var(--font-size-sm);
    color: var(--color-text-secondary);
    font-style: italic;
}

/* Confirmación de eliminar */
.confirm-eliminar {
    text-align: center;
    padding: var(--space-2) 0;
}

.confirm-icono {
    color: #ff6b6b;
    margin-bottom: var(--space-4);
}

.confirm-aviso {
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
    margin-bottom: var(--space-6);
}

.confirm-acciones {
    display: flex;
    gap: var(--space-3);
    justify-content: center;
}

.btn-eliminar {
    background: #ff6b6b !important;
    border-color: #ff6b6b !important;
    color: #fff !important;
}

@media (max-width: 700px) {

    .td-fecha,
    .col-acciones th:nth-child(3) {
        display: none;
    }
}
</style>