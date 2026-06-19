<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { userService } from '@/services/userService'
import type { Profile } from '@/types'
import { onMounted, ref } from 'vue'

const profile = ref<Profile | null>(null)
const bio = ref('')
const loading = ref(true)
const saving = ref(false)
const mensaje = ref('')

onMounted(async () => {
    try {
        const response = await userService.getProfile()
        profile.value = response.data
        bio.value = response.data.bio
    } finally {
        loading.value = false
    }
})

async function guardarCambios() {
    saving.value = true
    mensaje.value = ''
    try {
        const response = await userService.updateProfile({ bio: bio.value })
        profile.value = response.data
        mensaje.value = 'Perfil actualizado correctamente'
    } catch {
        mensaje.value = 'Error al actualizar el perfil'
    } finally {
        saving.value = false
    }
}
</script>

<template>
    <div class="profile-view">
        <h1>Mi perfil</h1>

        <div v-if="loading">Cargando...</div>

        <div v-else-if="profile" class="contenido">
            <p class="username">{{ profile.username }}</p>
            <p class="email">{{ profile.email }}</p>

            <div class="campo">
                <label for="bio">Bio</label>
                <textarea id="bio" v-model="bio" rows="4"></textarea>
            </div>

            <p v-if="mensaje" class="mensaje">{{ mensaje }}</p>

            <AppButton @click="guardarCambios" :disabled="saving">
                {{ saving ? 'Guardando...' : 'Guardar cambios' }}
            </AppButton>
        </div>
    </div>
</template>

<style scoped>
.profile-view {
    max-width: 500px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
}

.username {
    font-size: var(--font-size-xl);
    font-weight: bold;
}

.email {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-6);
}

.campo {
    margin-bottom: var(--space-4);
    text-align: left;
}

.campo label {
    display: block;
    margin-bottom: var(--space-1);
    color: var(--color-text-secondary);
}

.campo textarea {
    width: 100%;
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
    font-family: var(--font-sans);
}

.mensaje {
    color: var(--color-header-bg);
    margin-bottom: var(--space-4);
}
</style>