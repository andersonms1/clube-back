<template>
  <q-card
    class="task-card q-mb-md cursor-pointer"
    :class="{ 'dragging': isDragging }"
    draggable="true"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
  >
    <q-card-section>
      <div class="text-h6">{{ task.titulo }}</div>
      <div class="text-subtitle2">{{ formatDate(task.data_vencimento) }}</div>
    </q-card-section>

    <q-card-section>
      <p class="task-description">{{ task.descricao }}</p>
    </q-card-section>

    <q-card-actions align="right">
      <q-btn flat color="primary" icon="edit" @click="$emit('edit', task)" />
      <q-btn flat color="negative" icon="delete" @click="$emit('delete', task)" />
    </q-card-actions>
  </q-card>
</template>

<script setup lang="ts">
// import { computed } from 'vue';
import { Task } from '@/types';

const props = defineProps<{
  task: Task;
  isDragging?: boolean;
}>();

const emit = defineEmits<{
  (e: 'edit', task: Task): void;
  (e: 'delete', task: Task): void;
  (e: 'dragstart', task: Task): void;
  (e: 'dragend'): void;
}>();

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('pt-BR', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

function onDragStart(event: DragEvent) {
  if (event.dataTransfer) {
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', props.task.id);
  }
  emit('dragstart', props.task);
}

function onDragEnd() {
  emit('dragend');
}
</script>

<style scoped>
.task-card {
  transition: all 0.3s ease;
  min-height: 150px;
}

.task-card.dragging {
  opacity: 0.5;
  transform: scale(0.95);
}

.task-description {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}
</style>
