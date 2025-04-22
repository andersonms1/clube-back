import { ApiError } from '@/types';
import { useAuthStore } from '@/stores/auth';
import router from '@/router';
import { Notify } from 'quasar';

const API_URL = import.meta.env.VITE_API_URL
/**
 * Generic fetch function with error handling
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    // Get token from localStorage
    const token = localStorage.getItem('token');

    // Set default headers
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    };

    // Make the request
    const response = await fetch(`${API_URL}${endpoint}`, {
      ...options,
      headers,
    });

    // Parse the JSON response
    const data = await response.json();

    // Check if the response is ok
    if (!response.ok) {
      // Handle token expiration (401 Unauthorized)
      if (response.status === 401) {
        // Get auth store and handle logout
        const authStore = useAuthStore();
        authStore.cleanCredentials();

        // Show notification
        Notify.create({
          type: 'warning',
          message: 'Your session has expired. Please log in again.',
          icon: 'warning'
        });

        // Redirect to login page
        router.push('/login');
      }

      // Extract and format validation error messages
      let errorMessage = data.message || 'An error occurred';

      // Handle Pydantic validation errors which often come in a specific format
      if (errorMessage.includes('validation error')) {
        // Keep the error message as is, as it already contains the validation details
      } else {
        // For other types of errors, just use the message as is
      }

      throw {
        message: errorMessage,
        status: response.status,
      } as ApiError;
    }

    return data as T;
  } catch (error) {
    if (error instanceof Error) {
      throw {
        message: error.message,
        status: 500,
      } as ApiError;
    }
    throw error;
  }
}

/**
 * HTTP GET request
 */
export function get<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  return fetchApi<T>(endpoint, {
    method: 'GET',
    ...options,
  });
}

/**
 * HTTP POST request
 */
export function post<T>(
  endpoint: string,
  data: any,
  options: RequestInit = {}
): Promise<T> {
  return fetchApi<T>(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
    ...options,
  });
}

/**
 * HTTP PUT request
 */
export function put<T>(
  endpoint: string,
  data: any,
  options: RequestInit = {}
): Promise<T> {
  return fetchApi<T>(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
    ...options,
  });
}

/**
 * HTTP DELETE request
 */
export function del<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  return fetchApi<T>(endpoint, {
    method: 'DELETE',
    ...options,
  });
}

export default {
  get,
  post,
  put,
  delete: del,
};
