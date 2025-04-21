<template>
  <q-page padding>
    <div class="q-mb-lg">
      <div class="row justify-between items-center">
        <h1 class="text-h4 q-my-none">My Tasks</h1>
        <q-btn
          color="primary"
          icon="add"
          label="New Task"
          @click="openTaskDialog()"
        />
      </div>
    </div>

    <!-- Desktop View: Columns -->
    <div v-if="!screenSize.isMobile" class="row q-col-gutter-md">
      <div class="col-12 col-md-4">
        <TaskColumn
          title="Pending"
          status="pending"
          :tasks="tasksStore.pendingTasks"
          :dragged-task="draggedTask"
          @dragstart="onDragStart"
          @dragend="onDragEnd"
          @drop="onDrop"
          @edit="openTaskDialog"
          @delete="confirmDeleteTask"
        />
      </div>
      
      <div class="col-12 col-md-4">
        <TaskColumn
          title="In Progress"
          status="in_progress"
          :tasks="tasksStore.inProgressTasks"
          :dragged-task="draggedTask"
          @dragstart="onDragStart"
          @dragend="onDragEnd"
          @drop="onDrop"
          @edit="openTaskDialog"
          @delete="confirmDeleteTask"
        />
      </div>
      
      <div class="col-12 col-md-4">
        <TaskColumn
          title="Completed"
          status="completed"
          :tasks="tasksStore.completedTasks"
          :dragged-task="draggedTask"
          @dragstart="onDragStart"
          @dragend="onDragEnd"
          @drop="onDrop"
          @edit="openTaskDialog"
          @delete="confirmDeleteTask"
        />
      </div>
    </div>

    <!-- Mobile View: Tabs -->
    <div v-else>
      <q-tabs
        v-model="activeTab"
        class="text-primary"
        active-color="primary"
        indicator-color="primary"
        align="justify"
        narrow-indicator
      >
        <q-tab name="pending" label="Pending" />
        <q-tab name="in_progress" label="In Progress" />
        <q-tab name="completed" label="Completed" />
      </q-tabs>

      <q-separator />

      <q-tab-panels v-model="activeTab" animated>
        <q-tab-panel name="pending">
          <div v-if="tasksStore.pendingTasks.length === 0" class="text-center q-pa-lg">
            <q-icon name="inbox" size="3rem" color="grey-5" />
            <p class="text-grey-6">No pending tasks</p>
          </div>
          <div v-else>
            <TaskCard
              v-for="task in tasksStore.pendingTasks"
              :key="task.id"
              :task="task"
              @edit="openTaskDialog"
              @delete="confirmDeleteTask"
            />
          </div>
        </q-tab-panel>

        <q-tab-panel name="in_progress">
          <div v-if="tasksStore.inProgressTasks.length === 0" class="text-center q-pa-lg">
            <q-icon name="inbox" size="3rem" color="grey-5" />
            <p class="text-grey-6">No tasks in progress</p>
          </div>
          <div v-else>
            <TaskCard
              v-for="task in tasksStore.inProgressTasks"
              :key="task.id"
              :task="task"
              @edit="openTaskDialog"
              @delete="confirmDeleteTask"
            />
          </div>
        </q-tab-panel>

        <q-tab-panel name="completed">
          <div v-if="tasksStore.completedTasks.length === 0" class="text-center q-pa-lg">
            <q-icon name="inbox" size="3rem" color="grey-5" />
            <p class="text-grey-6">No completed tasks</p>
          </div>
          <div v-else>
            <TaskCard
              v-for="task in tasksStore.completedTasks"
              :key="task.id"
              :task="task"
              @edit="openTaskDialog"
              @delete="confirmDeleteTask"
            />
          </div>
        </q-tab-panel>
      </q-tab-panels>
    </div>

    <!-- Task Dialog -->
    <q-dialog v-model="taskDialog" persistent>
      <q-card style="min-width: 350px; max-width: 500px;">
        <q-card-section>
          <div class="text-h6">{{ editingTask ? 'Edit Task' : 'New Task' }}</div>
        </q-card-section>

        <q-card-section>
          <TaskForm
            :task="editingTask"
            :loading="tasksStore.loading"
            @submit="handleTaskSubmit"
            @cancel="taskDialog = false"
          />
        </q-card-section>
      </q-card>
    </q-dialog>

    <!-- Delete Confirmation Dialog -->
    <q-dialog v-model="deleteDialog" persistent>
      <q-card>
        <q-card-section class="row items-center">
          <q-avatar icon="delete" color="negative" text-color="white" />
          <span class="q-ml-sm">Are you sure you want to delete this task?</span>
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="Cancel" color="primary" v-close-popup />
          <q-btn
            flat
            label="Delete"
            color="negative"
            @click="deleteTask"
            :loading="tasksStore.loading"
            v-close-popup
          />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTasksStore } from '@/stores';
import { useScreenSize } from '@/composables';
import { useDragDrop } from '@/composables';
import { TaskCard, TaskColumn, TaskForm } from '@/components';
import { Task, TaskCreate, TaskUpdate, TaskStatus } from '@/types';

const tasksStore = useTasksStore();
const screenSize = useScreenSize();
const { draggedTask, onDragStart, onDragEnd, onDrop } = useDragDrop();

// For mobile tabs
const activeTab = ref<TaskStatus>('pending');

// Task dialog
const taskDialog = ref(false);
const editingTask = ref<Task | null | undefined>(null);

// Delete dialog
const deleteDialog = ref(false);
const taskToDelete = ref<Task | null>(null);

onMounted(async () => {
  await tasksStore.fetchTasks();
});

function openTaskDialog(task?: Task) {
  editingTask.value = task || null;
  taskDialog.value = true;
}

async function handleTaskSubmit(taskData: TaskCreate | TaskUpdate) {
  if (editingTask.value) {
    await tasksStore.updateTask(editingTask.value.id, taskData as TaskUpdate);
  } else {
    await tasksStore.createTask(taskData as TaskCreate);
  }
  
  taskDialog.value = false;
  editingTask.value = null;
}

function confirmDeleteTask(task: Task) {
  taskToDelete.value = task;
  deleteDialog.value = true;
}

async function deleteTask() {
  if (taskToDelete.value) {
    await tasksStore.deleteTask(taskToDelete.value.id);
    taskToDelete.value = null;
  }
}
</script>
