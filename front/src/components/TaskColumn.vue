<template>
  <div 
    class="task-column"
    :class="{ 'drop-active': isDropActive }"
    @dragover.prevent="onDragOver"
    @dragleave="onDragLeave"
    @drop.prevent="onDrop"
  >
    <div class="column-header q-pa-md">
      <h5 class="q-my-none">{{ title }} ({{ tasks.length }})</h5>
    </div>
    
    <div class="column-content q-pa-md">
      <template v-if="tasks.length > 0">
        <TaskCard
          v-for="task in tasks"
          :key="task.id"
          :task="task"
          :is-dragging="() => isDraggin(draggedTask, task.id)"
          @dragstart="$emit('dragstart', task)"
          @dragend="$emit('dragend')"
          @edit="$emit('edit', task)"
          @delete="$emit('delete', task)"
        />
      </template>
      <div v-else class="empty-column">
        <q-icon name="inbox" size="3rem" color="grey-5" />
        <p class="text-grey-6">No tasks</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Task, TaskStatus } from '@/types';
import TaskCard from './TaskCard.vue';

const props = defineProps<{
  title: string;
  status: TaskStatus;
  tasks: Task[];
  draggedTask: Task | null;
}>();

const emit = defineEmits<{
  (e: 'dragstart', task: Task): void;
  (e: 'dragend'): void;
  (e: 'drop', status: TaskStatus): void;
  (e: 'edit', task: Task): void;
  (e: 'delete', task: Task): void;
}>();

const isDropActive = ref(false);

function isDraggin(task: Task | null , task_id: string):boolean | undefined{
  if (!task)
    return 
  if (task?.id === task_id)
    return true
  return 
}

function onDragOver(event: DragEvent) {
  if (event.dataTransfer) {
    event.dataTransfer.dropEffect = 'move';
  }
  isDropActive.value = true;
}

function onDragLeave() {
  isDropActive.value = false;
}

function onDrop() {
  isDropActive.value = false;
  emit('drop', props.status);
}
</script>

<style scoped>
.task-column {
  background-color: #f5f5f5;
  border-radius: 8px;
  min-height: 400px;
  display: flex;
  flex-direction: column;
  transition: background-color 0.2s ease;
}

.drop-active {
  background-color: #e0f2f1;
}

.column-header {
  border-bottom: 1px solid #e0e0e0;
}

.column-content {
  flex: 1;
  overflow-y: auto;
}

.empty-column {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}
</style>
