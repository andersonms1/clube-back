<template>
  <q-page class="flex flex-center">
    <div class="auth-container">
      <div class="text-center q-mb-lg">
        <h2 class="text-h4 q-mb-md">Create an Account</h2>
        <p class="text-subtitle1">Join us to manage your tasks efficiently.</p>
      </div>
      
      <RegisterForm
        :loading="authStore.loading"
        :error="authStore.error"
        @submit="handleRegister"
        @login="$router.push('/login')"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import { RegisterForm } from '@/components';
import { UserRegistration } from '@/types';

const router = useRouter();
const authStore = useAuthStore();

onMounted(() => {
  // Clear any previous errors
  authStore.error = null;
});

async function handleRegister(userData: UserRegistration) {
  const success = await authStore.register(userData);
  if (success) {
    router.push('/');
  }
}
</script>

<style scoped>
.auth-container {
  width: 100%;
  max-width: 450px;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  background-color: white;
}

@media (max-width: 600px) {
  .auth-container {
    max-width: 90%;
    padding: 1.5rem;
  }
}
</style>
