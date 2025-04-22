import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { authApi } from '@/client';
import { User, UserCredentials, UserRegistration } from '@/types';
// import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const token = ref<string | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => !!token.value);

  // Initialize state from localStorage
  function init() {
    const storedToken = localStorage.getItem('token');
    const storedUser = localStorage.getItem('user');

    if (storedToken && storedUser) {
      token.value = storedToken;
      try {
        user.value = JSON.parse(storedUser);
      } catch (e) {
        // If parsing fails, clear localStorage
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      }
    }
  }

  // Actions
  async function login(credentials: UserCredentials) {
    loading.value = true;
    error.value = null;

    try {
      const response = await authApi.login(credentials);

      // Store token and user in state and localStorage
      token.value = response.access_token;
      user.value = response.user;

      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));

      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to login';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function register(userData: UserRegistration) {
    loading.value = true;
    error.value = null;

    try {
      const response = await authApi.register(userData);

      // Store token and user in state and localStorage
      token.value = response.access_token;
      user.value = response.user;

      localStorage.setItem('token', response.access_token);
      localStorage.setItem('user', JSON.stringify(response.user));

      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to register';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function cleanCredentials() {
    error.value = null;
    // Clear state and localStorage
    token.value = null;
    user.value = null;

    localStorage.removeItem('token');
    localStorage.removeItem('user');

    loading.value = false;
  }

  async function logout() {
    loading.value = true;
    error.value = null;

    try {
      // Call logout API
      await authApi.logout();
    } catch (err) {
      // Even if API call fails, we still want to clear local state
      console.error('Logout API call failed:', err);
    } finally {
      cleanCredentials()
    }
  }

  async function requestPasswordReset(email: string) {
    loading.value = true;
    error.value = null;

    try {
      await authApi.requestPasswordReset(email);
      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to request password reset';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function resetPassword(token: string, password: string) {
    loading.value = true;
    error.value = null;

    try {
      await authApi.resetPassword(token, password);
      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to reset password';
      return false;
    } finally {
      loading.value = false;
    }
  }

  // Initialize on store creation
  init();

  return {
    // State
    user,
    token,
    loading,
    error,

    // Getters
    isAuthenticated,

    // Actions
    login,
    register,
    logout,
    requestPasswordReset,
    resetPassword,
    cleanCredentials
  };
});
