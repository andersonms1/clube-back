import api from './api';
import { AuthResponse, UserCredentials, UserRegistration } from '@/types';

/**
 * Authentication API client
 */
export const authApi = {
  /**
   * Login with email and password
   */
  login(credentials: UserCredentials): Promise<AuthResponse> {
    return api.post<AuthResponse>('/api/auth/login', credentials);
  },

  /**
   * Register a new user
   */
  register(userData: UserRegistration): Promise<AuthResponse> {
    return api.post<AuthResponse>('/api/users', userData);
  },

  /**
   * Logout the current user
   */
  logout(): Promise<{ message: string }> {
    return api.post<{ message: string }>('/api/auth/logout', {});
  },

  /**
   * Request password reset
   */
  requestPasswordReset(email: string): Promise<{ message: string }> {
    return api.post<{ message: string }>('/api/auth/reset-password', { email });
  },

  /**
   * Reset password with token
   */
  resetPassword(token: string, password: string): Promise<{ message: string }> {
    return api.post<{ message: string }>(`/api/auth/reset-password/${token}`, { password });
  },
};

export default authApi;
