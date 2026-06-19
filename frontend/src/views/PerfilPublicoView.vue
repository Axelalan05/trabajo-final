<script setup lang="ts">
import { userService } from '@/services/userService'
import type { Profile } from '@/types'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const profile = ref<Profile | null>(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
    try {
        const username = route.params.username as string
        const response = await userService.getProfilePublico(username)
        profile.value = response.data
    } catch {
        error.value = 'Usuario no encontrado'
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <div class="perfil-publico-view">
        <div v-if="loading">Cargando...</div>
        <div v-else-if="error" class="error">{{ error }}</div>
        <div v-else-if="profile" class="contenido">
            <h1>{{ profile.username }}</h1>
            <p v-if="profile.bio">{{ profile.bio }}</p>
            <p v-else class="sin-bio">Este usuario no tiene bio.</p>
        </div>
    </div>
</template>

<style scoped>
.perfil-publico-view {
    max-width: 500px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
    text-align: center;
}

.sin-bio {
    color: var(--color-text-secondary);
}

.error {
    color: #ff6b6b;
}
</style>