<script setup lang="ts">
import AppButton from '@/components/ui/AppButton.vue'
import api from '@/services/api'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const error = ref('')
const loading = ref(false)
const registrado = ref(false)

async function handleRegister() {
    error.value = ''
    loading.value = true
    try {
        const response = await api.post('/auth/register/', {
            username: username.value,
            email: email.value,
            password: password.value,
            password_confirm: passwordConfirm.value,
        })
        registrado.value = true
        console.log('⚠️ Enlace de verificación:', response.data.data.verification_url)  // ← agregá esto
    } catch (err: any) {
        const data = err?.response?.data
        const details = data?.error?.details
        if (details) {
            if (typeof details === 'object') {
                error.value = Object.values(details).flat().join(', ')
            } else {
                error.value = String(details)
            }
        } else {
            error.value = data?.error?.message || 'Error al registrarse'
        }
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <div class="register-view">
        <template v-if="!registrado">
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
                    <div class="campo">
                        <label for="password">Contraseña</label>
                        <input id="password" v-model="password" type="password" required />
                        <p class="requisitos-password">
                            Mínimo 8 caracteres, una mayúscula, un número y, opcionalmente, un símbolo.
                        </p>
                    </div>
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
        </template>

        <template v-else>
            <div class="verificacion-email">
                <div class="icono-email">✉️</div>
                <h1>Revisá tu correo</h1>
                <p class="mensaje-verificacion">
                    Te enviamos un enlace de confirmación a <strong>{{ email }}</strong>.
                </p>
                <p class="mensaje-verificacion">
                    Hacé clic en el enlace del correo para activar tu cuenta.
                    Si no lo recibiste en unos minutos, revisá la carpeta de spam.
                </p>
                <p class="mensaje-no-recibido">
                    ¿No recibiste el correo?
                    <button class="reenviar-btn" @click="handleRegister" :disabled="loading">
                        Reenviar
                    </button>
                </p>
                <router-link to="/login" class="link-login">Volver al inicio de sesión</router-link>
            </div>
        </template>
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

.requisitos-password {
    margin: var(--space-1) 0 0;
    color: var(--color-text-secondary);
    font-size: var(--font-size-xs);
    line-height: 1.4;
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

.verificacion-email {
    text-align: center;
    padding: var(--space-8) 0;
}

.icono-email {
    font-size: 48px;
    margin-bottom: var(--space-4);
}

.mensaje-verificacion {
    color: var(--color-text-secondary);
    line-height: 1.6;
    margin-bottom: var(--space-4);
}

.mensaje-no-recibido {
    color: var(--color-text-secondary);
    margin-top: var(--space-6);
    margin-bottom: var(--space-4);
}

.reenviar-btn {
    background: none;
    border: none;
    color: var(--color-header-bg);
    cursor: pointer;
    font-size: inherit;
    font-family: var(--font-sans);
    text-decoration: underline;
}

.reenviar-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.link-login {
    color: var(--color-header-bg);
    display: inline-block;
    margin-top: var(--space-2);
}
</style>
