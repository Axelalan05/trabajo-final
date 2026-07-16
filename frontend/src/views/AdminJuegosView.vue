<script setup lang="ts">
import JuegoForm from '@/components/juegos/JuegoForm.vue'
import AppButton from '@/components/ui/AppButton.vue'
import AppModal from '@/components/ui/AppModal.vue'
import { juegoService } from '@/services/juegoService'
import type { Juego } from '@/types'
import { Pencil, Plus, Trash2 } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'

const juegos = ref<Juego[]>([])
const loading = ref(true)
const showModal = ref(false)
const juegoEditando = ref<Juego | null>(null)
const errorSubmit = ref('')

async function cargarJuegos() {
    loading.value = true
    try {
        const response = await juegoService.listCatalogo()
        juegos.value = response.data
    } finally {
        loading.value = false
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
    await juegoService.delete(id)
    juegos.value = juegos.value.filter((j) => j.id !== id)
}

onMounted(cargarJuegos)
</script>

<template>
    <div class="admin-juegos-view">
        <div class="encabezado">
            <h1>Administrar catálogo</h1>
            <AppButton @click="abrirModalCrear">
                <Plus :size="18" /> Agregar juego
            </AppButton>
        </div>

        <div v-if="loading">Cargando...</div>

        <div v-else-if="juegos.length === 0" class="vacio">
            Todavía no hay juegos en el catálogo.
        </div>

        <div v-else class="lista-juegos">
            <div v-for="juego in juegos" :key="juego.id" class="juego-card">
                <h3>{{ juego.nombre }}</h3>
                <p class="detalle">{{ juego.genero }} · {{ juego.plataforma }} · {{ juego.anio }}</p>
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
</style>