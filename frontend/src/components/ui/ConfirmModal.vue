<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue';
import AppModal from '@/components/ui/AppModal.vue';

withDefaults(
    defineProps<{
        show: boolean
        title: string
        mensaje: string
        textoConfirmar?: string
        variantConfirmar?: 'primary' | 'secondary' | 'danger'
    }>(),
    {
        textoConfirmar: 'Confirmar',
        variantConfirmar: 'primary',
    }
)

const emit = defineEmits<{
    confirm: []
    close: []
}>()
</script>

<template>
    <AppModal :show="show" :title="title" @close="emit('close')">
        <p class="mensaje">{{ mensaje }}</p>
        <div class="acciones">
            <AppButton variant="secondary" @click="emit('close')">Cancelar</AppButton>
            <AppButton :variant="variantConfirmar" @click="emit('confirm')">{{ textoConfirmar }}</AppButton>
        </div>
    </AppModal>
</template>

<style scoped>
.mensaje {
    margin-bottom: var(--space-4);
}

.acciones {
    display: flex;
    justify-content: flex-end;
    gap: var(--space-3);
}
</style>