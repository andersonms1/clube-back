import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { tasksApi } from '@/client';
import { Task, TaskCreate, TaskUpdate, TaskStatus } from '@/types';

export const useTasksStore = defineStore('tasks', () => {
  // State
  const tasks = ref<Task[]>([]);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const getTaskById = computed(() => (id: string) => {
    return tasks.value.find(task => task.id === id);
  });

  const getTasksByStatus = computed(() => (status: TaskStatus) => {
    return tasks.value.filter(task => task.status === status);
  });

  const pendingTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'pending');
  });

  const inProgressTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'in_progress');
  });

  const completedTasks = computed(() => {
    return tasks.value.filter(task => task.status === 'completed');
  });

  // Actions
  async function fetchTasks() {
    loading.value = true;
    error.value = null;

    try {
      const response = await tasksApi.getAllTasks();
      tasks.value = response;
      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch tasks';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function fetchTask(id: string) {
    loading.value = true;
    error.value = null;

    try {
      const response = await tasksApi.getTask(id);

      // Update the task in the tasks array if it exists
      const index = tasks.value.findIndex(task => task.id === id);
      if (index !== -1) {
        tasks.value[index] = response;
      } else {
        tasks.value.push(response);
      }

      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch task';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function createTask(taskData: TaskCreate) {
    loading.value = true;
    error.value = null;

    try {
      const response = await tasksApi.createTask(taskData);
      tasks.value.push(response);
      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to create task';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function updateTask(id: string, taskData: TaskUpdate) {
    loading.value = true;
    error.value = null;

    try {
      const response = await tasksApi.updateTask(id, taskData);

      // Update the task in the tasks array
      const index = tasks.value.findIndex(task => task.id === id);
      if (index !== -1) {
        tasks.value[index] = response;
      }

      return response;
    } catch (err: any) {
      error.value = err.message || 'Failed to update task';
      return null;
    } finally {
      loading.value = false;
    }
  }

  async function deleteTask(id: string) {
    loading.value = true;
    error.value = null;

    try {
      await tasksApi.deleteTask(id);

      // Remove the task from the tasks array
      tasks.value = tasks.value.filter(task => task.id !== id);

      return true;
    } catch (err: any) {
      error.value = err.message || 'Failed to delete task';
      return false;
    } finally {
      loading.value = false;
    }
  }

  async function changeTaskStatus(id: string, status: TaskStatus) {
    return updateTask(id, { status });
  }

  return {
    // State
    tasks,
    loading,
    error,

    // Getters
    getTaskById,
    getTasksByStatus,
    pendingTasks,
    inProgressTasks,
    completedTasks,

    // Actions
    fetchTasks,
    fetchTask,
    createTask,
    updateTask,
    deleteTask,
    changeTaskStatus
  };
});
