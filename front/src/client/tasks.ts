import api from './api';
import { Task, TaskCreate, TaskUpdate } from '@/types';

/**
 * Tasks API client
 */
export const tasksApi = {
  /**
   * Get all tasks for the current user
   */
  getAllTasks(): Promise<Task[]> {
    return api.get<Task[]>('/api/tasks');
  },

  /**
   * Get a specific task by ID
   */
  getTask(id: string): Promise<Task> {
    return api.get<Task>(`/api/tasks/${id}`);
  },

  /**
   * Create a new task
   */
  createTask(task: TaskCreate): Promise<Task> {
    return api.post<Task>('/api/tasks', task);
  },

  /**
   * Update an existing task
   */
  updateTask(id: string, task: TaskUpdate): Promise<Task> {
    return api.put<Task>(`/api/tasks/${id}`, task);
  },

  /**
   * Delete a task
   */
  deleteTask(id: string): Promise<{ message: string }> {
    return api.delete<{ message: string }>(`/api/tasks/${id}`);
  },
};

export default tasksApi;
