<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
    error.value = ''
    loading.value = true
    try {
        await authStore.register(username.value, email.value, password.value, passwordConfirm.value)
        router.push('/login')
    } catch (err: any) {
        const data = err?.response?.data
        error.value = data?.error?.message || 'Error al registrarse'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="register-view">
        <h1>Crear cuenta</h1>
        <form @submit.prevent="handleRegister">
            <div class="campo">
                <label for="username">Usuario</label>
                <input id="username" v-model="username" type="text" required />
            </div>
            <div class="campo">
                <label for="email">Email</label>
                <input id="email" v-model="email" type="email" required />
            </div>
            <div class="campo">
                <label for="password">Contraseña</label>
                <input id="password" v-model="password" type="password" required />
            </div>
            <div class="campo">
                <label for="password_confirm">Confirmar contraseña</label>
                <input id="password_confirm" v-model="passwordConfirm" type="password" required />
            </div>
            <p v-if="error" class="error">{{ error }}</p>
            <AppButton type="submit" :disabled="loading">
                {{ loading ? 'Creando cuenta...' : 'Registrarme' }}
            </AppButton>
        </form>
        <p class="link-secundario">
            ¿Ya tenés cuenta? <router-link to="/login">Iniciá sesión</router-link>
        </p>
    </div>
</template>

<style scoped>
.register-view {
    max-width: 400px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
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

.campo input {
    width: 100%;
    padding: var(--space-2);
    border-radius: var(--radius-sm);
    border: none;
}

.error {
    color: #ff6b6b;
    margin-bottom: var(--space-4);
}

.link-secundario {
    color: var(--color-text-secondary);
    margin-top: var(--space-4);
}

.link-secundario a {
    color: var(--color-header-bg);
}
</style>