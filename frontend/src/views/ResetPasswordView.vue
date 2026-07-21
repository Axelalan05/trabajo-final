<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import { confirmPasswordReset } from '@/services/api'
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const uid = Number(route.params.uid)
const token = route.params.token as string

const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
    error.value = ''
    loading.value = true
    try {
        await confirmPasswordReset(uid, token, password.value, passwordConfirm.value)
        router.push({ name: 'login', query: { reset: 'success' } })
    } catch (err: any) {
        const details = err?.response?.data?.details
        if (details?.token) {
            error.value = 'El enlace es inválido o ha expirado. Solicitá uno nuevo.'
        } else if (details?.password_confirm) {
            error.value = details.password_confirm[0]
        } else {
            error.value = err?.response?.data?.message || 'Error al restablecer la contraseña.'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="reset-password-view">
        <h1>Restablecer contraseña</h1>
        <p class="descripcion">Ingresá tu nueva contraseña.</p>
        <form @submit.prevent="handleSubmit">
            <div class="campo">
                <label for="password">Nueva contraseña</label>
                <input id="password" v-model="password" type="password" required minlength="8"
                    placeholder="Mínimo 8 caracteres" />
            </div>
            <div class="campo">
                <label for="password-confirm">Repetir contraseña</label>
                <input id="password-confirm" v-model="passwordConfirm" type="password" required minlength="8"
                    placeholder="Repetí la contraseña" />
            </div>
            <p v-if="error" class="error">{{ error }}</p>
            <AppButton type="submit" :disabled="loading">
                {{ loading ? 'Guardando...' : 'Guardar nueva contraseña' }}
            </AppButton>
        </form>
    </div>
</template>

<style scoped>
.reset-password-view {
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
</style>
