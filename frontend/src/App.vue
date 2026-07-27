<script setup lang="ts">
import AppLayout from '@/layouts/AppLayout.vue';
import { RouterView } from 'vue-router';
</script>

<template>
  <AppLayout>
    <RouterView v-slot="{ Component, route }">
      <Transition name="page" mode="out-in">
        <component :is="Component" :key="route.path" />
      </Transition>
    </RouterView>
  </AppLayout>
</template>