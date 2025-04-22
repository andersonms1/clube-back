<template>
  <q-page class="flex flex-center">
    <div class="auth-container">
      <div class="text-center q-mb-lg">
        <h2 class="text-h4 q-mb-md">Reset Your Password</h2>
        <p class="text-subtitle1">
          Enter your new password below.
        </p>
      </div>
      
      <ResetPasswordForm
        :token="token"
        :loading="authStore.loading"
        :error="authStore.error"
        @submit-password="handleResetPassword"
        @login="$router.push('/login')"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '@/stores';
import { ResetPasswordForm } from '@/components';
import { Notify } from 'quasar';


const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const token = ref<string>(route.params.token as string);

onMounted(() => {
  // Clear any previous errors
  authStore.error = null;
  
  // Validate token
  if (!token.value) {
    router.push('/reset-password');
  }
});

async function handleResetPassword(password: string) {
  const success = await authStore.resetPassword(token.value, password);
  if (success) {
    authStore.error = null;
    // Show success message
    Notify.create({
      type: 'positive',
      message: 'Your password has been reset successfully.',
      icon: 'thumb_up'
    });
    router.push('/login');
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
