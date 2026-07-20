<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue';
import type { Juego } from '@/types';
import { ref, watch } from 'vue';

const props = defineProps<{
    juego?: Partial<Juego> | null
}>()

const emit = defineEmits<{
    submit: [data: Partial<Juego>]
}>()

const rawgId = ref<number | null>(null)
const nombre = ref('')
const genero = ref('')
const plataforma = ref('')
const descripcion = ref('')
const fechaLanzamiento = ref('')
const imagenUrl = ref('')

watch(
    () => props.juego,
    (juego) => {
        rawgId.value = juego?.rawg_id ?? null
        nombre.value = juego?.nombre ?? ''
        genero.value = juego?.genero ?? ''
        plataforma.value = juego?.plataforma ?? ''
        descripcion.value = juego?.descripcion ?? ''
        fechaLanzamiento.value = juego?.fecha_lanzamiento ?? ''
        imagenUrl.value = juego?.imagen_url ?? ''
    },
    { immediate: true }
)

function handleSubmit() {
    emit('submit', {
        rawg_id: rawgId.value,
        nombre: nombre.value,
        genero: genero.value,
        plataforma: plataforma.value,
        descripcion: descripcion.value,
        fecha_lanzamiento: fechaLanzamiento.value || null,
        imagen_url: imagenUrl.value || null,
    })
}
</script>

<template>
    <form class="juego-form" @submit.prevent="handleSubmit">
        <img v-if="imagenUrl" :src="imagenUrl" alt="" class="portada-preview" />

        <div class="campo">
            <label for="nombre">Nombre</label>
            <input id="nombre" v-model="nombre" type="text" required />
        </div>

        <div class="campo">
            <label for="genero">Género</label>
            <input id="genero" v-model="genero" type="text" required placeholder="Ej: Action, RPG" />
        </div>

        <div class="campo">
            <label for="plataforma">Plataforma</label>
            <input id="plataforma" v-model="plataforma" type="text" required placeholder="Ej: PC, PlayStation 5" />
        </div>

        <div class="campo">
            <label for="fecha">Fecha de lanzamiento</label>
            <input id="fecha" v-model="fechaLanzamiento" type="date" />
        </div>

        <div class="campo">
            <label for="imagen">URL de la portada</label>
            <input id="imagen" v-model="imagenUrl" type="url" placeholder="https://..." />
        </div>

        <div class="campo">
            <label for="descripcion">Descripción</label>
            <textarea id="descripcion" v-model="descripcion" rows="4"></textarea>
        </div>

        <AppButton type="submit">
            {{ props.juego?.id ? 'Guardar cambios' : 'Agregar juego' }}
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

.portada-preview {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: var(--radius-md);
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
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: var(--color-footer-bg);
    color: var(--color-text);
    font-family: var(--font-sans);
    box-sizing: border-box;
}

.campo input:focus,
.campo select:focus,
.campo textarea:focus {
    outline: none;
    border-color: var(--color-header-bg);
}

.campo input::placeholder {
    color: var(--color-text-secondary);
}
</style>