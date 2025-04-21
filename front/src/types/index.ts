// User types
export interface User {
  id: string;
  email: string;
  username: string;
}

export interface UserCredentials {
  email: string;
  password: string;
}

export interface UserRegistration extends UserCredentials {
  username: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
}

// Task types
export interface Task {
  id: string;
  titulo: string;
  descricao: string;
  status: TaskStatus;
  data_vencimento: string;
  user_id: string;
}

export type TaskStatus = 'pending' | 'in_progress' | 'completed';

export interface TaskCreate {
  titulo: string;
  descricao: string;
  status: TaskStatus;
  data_vencimento: string;
}

export interface TaskUpdate {
  titulo?: string;
  descricao?: string;
  status?: TaskStatus;
  data_vencimento?: string;
}

// API response types
export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface ApiError {
  message: string;
  status?: number;
}
