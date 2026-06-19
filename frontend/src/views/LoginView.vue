<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
    error.value = ''
    loading.value = true
    try {
        await authStore.login(username.value, password.value)
        router.push('/mis-juegos')
    } catch (err: any) {
        error.value = 'Usuario o contraseña incorrectos'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="login-view">
        <h1>Iniciar sesión</h1>
        <form @submit.prevent="handleLogin">
            <div class="campo">
                <label for="username">Usuario</label>
                <input id="username" v-model="username" type="text" required />
            </div>
            <div class="campo">
                <label for="password">Contraseña</label>
                <input id="password" v-model="password" type="password" required />
            </div>
            <p v-if="error" class="error">{{ error }}</p>
            <AppButton type="submit" :disabled="loading">
                {{ loading ? 'Ingresando...' : 'Ingresar' }}
            </AppButton>
        </form>
        <p class="link-secundario">
            ¿No tenés cuenta? <router-link to="/register">Registrate</router-link>
        </p>
    </div>
</template>

<style scoped>
.login-view {
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

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
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