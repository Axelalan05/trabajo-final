<script setup lang="ts">
const año = new Date().getFullYear()
</script>

<template>
    <footer class="app-footer">
        <p>© {{ año }} GameVault. Proyecto final — Universidad Nacional del Comahue.</p>
    </footer>
</template>

<style scoped>
.app-footer {
    background: var(--color-footer-bg);
    color: var(--color-footer-text);
    text-align: center;
    padding: var(--space-4);
    font-size: var(--font-size-sm);
}
</style>