<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { requestPasswordReset } from '@/services/api'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const email = ref('')
const error = ref('')
const success = ref('')
const loading = ref(false)

async function handleSubmit() {
    error.value = ''
    success.value = ''
    loading.value = true
    try {
        await requestPasswordReset(email.value)
        success.value = 'Si el correo está registrado, recibirás un enlace para restablecer tu contraseña.'
        email.value = ''
    } catch (err: any) {
        error.value = err?.response?.data?.message || 'Error al enviar la solicitud.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="forgot-password-view">
        <h1>Recuperar contraseña</h1>
        <p class="descripcion">
            Ingresá tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.
        </p>
        <form @submit.prevent="handleSubmit">
            <div class="campo">
                <label for="email">Correo electrónico</label>
                <input id="email" v-model="email" type="email" required placeholder="tu@email.com" />
            </div>
            <p v-if="error" class="error">{{ error }}</p>
            <p v-if="success" class="success">{{ success }}</p>
            <AppButton type="submit" :disabled="loading">
                {{ loading ? 'Enviando...' : 'Enviar enlace' }}
            </AppButton>
        </form>
        <p class="link-secundario">
            <router-link to="/login">Volver al inicio de sesión</router-link>
        </p>
    </div>
</template>

<style scoped>
.forgot-password-view {
    max-width: 400px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
}

.descripcion {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-6);
    text-align: center;
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
    border: 1px solid rgba(255, 255, 255, 0.15);
    background: var(--color-footer-bg);
    color: var(--color-text);
    font-family: var(--font-sans);
    box-sizing: border-box;
}

.campo input:focus {
    outline: none;
    border-color: var(--color-header-bg);
}

.campo input::placeholder {
    color: var(--color-text-secondary);
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.error {
    color: #ff6b6b;
    margin-bottom: var(--space-4);
}

.success {
    color: #51cf66;
    margin-bottom: var(--space-4);
}

.link-secundario {
    color: var(--color-text-secondary);
    margin-top: var(--space-4);
    text-align: center;
}

.link-secundario a {
    color: var(--color-header-bg);
}
</style>
