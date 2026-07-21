<script setup lang="ts">
import { ArrowUp } from 'lucide-vue-next'
import { onMounted, onUnmounted, ref } from 'vue'

const visible = ref(false)

function chequearScroll() {
    visible.value = window.scrollY > 400
}

function subirArriba() {
    window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
    window.addEventListener('scroll', chequearScroll, { passive: true })
})

onUnmounted(() => {
    window.removeEventListener('scroll', chequearScroll)
})
</script>

<template>
    <Transition name="fade">
        <button v-if="visible" class="back-to-top" aria-label="Volver arriba" @click="subirArriba">
            <ArrowUp :size="22" />
        </button>
    </Transition>
</template>

<style scoped>
.back-to-top {
    position: fixed;
    bottom: var(--space-6);
    right: var(--space-6);
    width: 48px;
    height: 48px;
    border-radius: var(--radius-full);
    border: none;
    background: var(--color-header-bg);
    color: var(--color-header-text);
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);
    transition: transform 0.15s ease, filter 0.15s ease;
    z-index: 20;
}

.back-to-top:hover {
    filter: brightness(1.1);
    transform: translateY(-2px);
}

.back-to-top:active {
    transform: scale(0.95);
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
    transform: translateY(10px);
}

@media (max-width: 600px) {
    .back-to-top {
        bottom: var(--space-4);
        right: var(--space-4);
        width: 44px;
        height: 44px;
    }
}
</style>