import { ref } from 'vue';
import { Task, TaskStatus } from '@/types';
import { useTasksStore } from '@/stores';

export function useDragDrop() {
  const draggedTask = ref<Task | null>(null);
  const tasksStore = useTasksStore();

  function onDragStart(task: Task) {
    draggedTask.value = task;
  }

  function onDragEnd() {
    draggedTask.value = null;
  }

  async function onDrop(status: TaskStatus) {
    if (!draggedTask.value) return;

    // Only update if the status is different
    if (draggedTask.value.status !== status) {
      await tasksStore.changeTaskStatus(draggedTask.value.id, status);
    }

    draggedTask.value = null;
  }

  return {
    draggedTask,
    onDragStart,
    onDragEnd,
    onDrop
  };
}
