<template>
  <q-page class="flex flex-center">
    <div class="auth-container">
      <div class="text-center q-mb-lg">
        <h2 class="text-h4 q-mb-md">Reset Password</h2>
        <p class="text-subtitle1" v-if="!token">
          Enter your email to receive a password reset link.
        </p>
        <p class="text-subtitle1" v-else>
          Enter your new password below.
        </p>
      </div>
      
      <ResetPasswordForm
        :token="token"
        :loading="authStore.loading"
        :error="authStore.error"
        @submit-email="handleResetRequest"
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

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const token = ref<string | undefined>(route.params.token as string | undefined);
const resetSuccess = ref(false);

onMounted(() => {
  // Clear any previous errors
  authStore.error = null;
});

async function handleResetRequest(email: string) {
  const success = await authStore.requestPasswordReset(email);
  if (success) {
    resetSuccess.value = true;
    authStore.error = null;
    // Show success message
    alert('Password reset link has been sent to your email.');
    router.push('/login');
  }
}

async function handleResetPassword(password: string) {
  if (!token.value) return;
  
  const success = await authStore.resetPassword(token.value, password);
  if (success) {
    resetSuccess.value = true;
    authStore.error = null;
    // Show success message
    alert('Your password has been reset successfully.');
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
