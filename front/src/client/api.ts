import { ApiError } from '@/types';

const API_URL = 'http://localhost:5000';

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
      throw {
        message: data.message || 'An error occurred',
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
