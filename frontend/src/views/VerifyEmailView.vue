<script setup lang="ts">
import api from '@/services/api'
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const uid = Number(route.params.uid)
const token = route.params.token as string

const estado = ref<'verificando' | 'exitoso' | 'error'>('verificando')
const mensaje = ref('')

onMounted(async () => {
    try {
        const { data } = await api.post('/auth/verify-email/', { uid, token })
        estado.value = 'exitoso'
        mensaje.value = data?.data?.message || 'Cuenta confirmada exitosamente.'
    } catch (err: any) {
        estado.value = 'error'
        mensaje.value = err?.response?.data?.error?.message || 'El enlace es inválido o ha expirado.'
    }
})
</script>

<template>
    <div class="verify-email-view">
        <template v-if="estado === 'verificando'">
            <h1>Verificando tu cuenta...</h1>
            <p class="mensaje">Por favor esperá un momento.</p>
        </template>

        <template v-else-if="estado === 'exitoso'">
            <div class="icono-exito">✅</div>
            <h1>¡Registrado exitosamente!</h1>
            <p class="mensaje">{{ mensaje }}</p>
            <router-link to="/login" class="btn-login">Iniciar sesión</router-link>
        </template>

        <template v-else>
            <div class="icono-error">❌</div>
            <h1>Error de verificación</h1>
            <p class="mensaje">{{ mensaje }}</p>
            <router-link to="/register" class="btn-login">Volver a registrarse</router-link>
        </template>
    </div>
</template>

<style scoped>
.verify-email-view {
    max-width: 450px;
    margin: var(--space-8) auto;
    padding: var(--space-6);
    color: var(--color-text);
    text-align: center;
}

.icono-exito,
.icono-error {
    font-size: 48px;
    margin-bottom: var(--space-4);
}

.mensaje {
    color: var(--color-text-secondary);
    margin-bottom: var(--space-6);
    line-height: 1.6;
}

.btn-login {
    display: inline-block;
    background-color: var(--color-header-bg);
    color: var(--color-header-text);
    padding: var(--space-2) var(--space-6);
    border-radius: var(--radius-md);
    text-decoration: none;
    font-weight: bold;
    transition: transform 0.15s ease;
}

.btn-login:hover {
    transform: translateY(-1px);
}
</style>
