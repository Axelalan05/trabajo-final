<script setup lang="ts">
import { ChevronLeft, ChevronRight } from 'lucide-vue-next';
import { computed } from 'vue';

const props = defineProps<{
    paginaActual: number
    totalPaginas: number
}>()

const emit = defineEmits<{
    'update:paginaActual': [pagina: number]
}>()

// Arma la lista de páginas a mostrar, usando '...' cuando hay muchas
const paginas = computed<(number | string)[]>(() => {
    const total = props.totalPaginas
    const actual = props.paginaActual
    const rango: (number | string)[] = []

    if (total <= 7) {
        for (let i = 1; i <= total; i++) rango.push(i)
        return rango
    }

    rango.push(1)
    if (actual > 3) rango.push('...')

    const desde = Math.max(2, actual - 1)
    const hasta = Math.min(total - 1, actual + 1)
    for (let i = desde; i <= hasta; i++) rango.push(i)

    if (actual < total - 2) rango.push('...')
    rango.push(total)

    return rango
})

function ir(pagina: number) {
    if (pagina < 1 || pagina > props.totalPaginas || pagina === props.paginaActual) return
    emit('update:paginaActual', pagina)
}
</script>

<template>
    <nav v-if="totalPaginas > 1" class="paginacion" aria-label="Paginación">
        <button class="pag-btn" :disabled="paginaActual === 1" @click="ir(paginaActual - 1)"
            aria-label="Página anterior">
            <ChevronLeft :size="18" />
        </button>

        <template v-for="(pagina, i) in paginas" :key="i">
            <span v-if="pagina === '...'" class="pag-puntos">…</span>
            <button v-else class="pag-btn" :class="{ 'pag-btn-activa': pagina === paginaActual }"
                @click="ir(pagina as number)">
                {{ pagina }}
            </button>
        </template>

        <button class="pag-btn" :disabled="paginaActual === totalPaginas" @click="ir(paginaActual + 1)"
            aria-label="Página siguiente">
            <ChevronRight :size="18" />
        </button>
    </nav>
</template>

<style scoped>
.paginacion {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--space-2);
    margin-top: var(--space-8);
    flex-wrap: wrap;
}

.pag-btn {
    min-width: 36px;
    height: 36px;
    padding: 0 var(--space-2);
    border-radius: var(--radius-sm);
    border: 1px solid var(--color-text-secondary);
    background: transparent;
    color: var(--color-text);
    font-family: var(--font-sans);
    font-weight: 500;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: background 0.15s ease, transform 0.15s ease, border-color 0.15s ease;
}

.pag-btn:hover:not(:disabled) {
    border-color: var(--color-header-bg);
    transform: translateY(-1px);
}

.pag-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
}

.pag-btn-activa {
    background: var(--color-header-bg);
    color: var(--color-header-text);
    border-color: var(--color-header-bg);
}

.pag-puntos {
    color: var(--color-text-secondary);
    padding: 0 var(--space-1);
}
</style>