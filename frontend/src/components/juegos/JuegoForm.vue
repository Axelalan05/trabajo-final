<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue';
import type { Juego } from '@/types';
import { ref, watch } from 'vue';

const props = defineProps<{
    juego?: Juego | null
}>()

const emit = defineEmits<{
    submit: [data: Partial<Juego>]
}>()

const nombre = ref('')
const genero = ref('')
const plataforma = ref('')
const descripcion = ref('')
const anio = ref<number | null>(null)
const estado = ref<Juego['estado']>('pendiente')
const puntaje = ref<number | null>(null)
const reseña = ref('')

watch(
    () => props.juego,
    (juego) => {
        if (juego) {
            nombre.value = juego.nombre
            genero.value = juego.genero
            plataforma.value = juego.plataforma
            descripcion.value = juego.descripcion
            anio.value = juego.anio
            estado.value = juego.estado
            puntaje.value = juego.puntaje
            reseña.value = juego.reseña
        }
    },
    { immediate: true }
)

function handleSubmit() {
    emit('submit', {
        nombre: nombre.value,
        genero: genero.value,
        plataforma: plataforma.value,
        descripcion: descripcion.value,
        anio: anio.value!,
        estado: estado.value,
        puntaje: puntaje.value,
        reseña: reseña.value,
    })
}
</script>

<template>
    <form class="juego-form" @submit.prevent="handleSubmit">
        <div class="campo">
            <label for="nombre">Nombre</label>
            <input id="nombre" v-model="nombre" type="text" required />
        </div>

        <div class="campo">
            <label for="genero">Género</label>
            <input id="genero" v-model="genero" type="text" required />
        </div>

        <div class="campo">
            <label for="plataforma">Plataforma</label>
            <input id="plataforma" v-model="plataforma" type="text" required />
        </div>

        <div class="campo">
            <label for="anio">Año</label>
            <input id="anio" v-model.number="anio" type="number" required />
        </div>

        <div class="campo">
            <label for="descripcion">Descripción</label>
            <textarea id="descripcion" v-model="descripcion" rows="3"></textarea>
        </div>

        <div class="campo">
            <label for="estado">Estado</label>
            <select id="estado" v-model="estado">
                <option value="pendiente">Pendiente</option>
                <option value="jugando">Jugando</option>
                <option value="completado">Completado</option>
                <option value="abandonado">Abandonado</option>
            </select>
        </div>

        <div class="campo">
            <label for="puntaje">Puntaje (1-10)</label>
            <input id="puntaje" v-model.number="puntaje" type="number" min="1" max="10" />
        </div>

        <div class="campo">
            <label for="resenia">Reseña</label>
            <textarea id="resenia" v-model="reseña" rows="3"></textarea>
        </div>

        <AppButton type="submit">
            {{ props.juego ? 'Guardar cambios' : 'Agregar juego' }}
        </AppButton>
    </form>
</template>

<style scoped>
.juego-form {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
    text-align: left;
}

.campo label {
    display: block;
    margin-bottom: var(--space-1);
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
}

.campo input,
.campo select,
.campo textarea {
    width: 100%;
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
    font-family: var(--font-sans);
    box-sizing: border-box;
}
</style>