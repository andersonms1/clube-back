<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <!-- Error alert -->
    <q-banner v-if="errorMessage" class="bg-negative text-white q-mb-md" rounded>
      {{ errorMessage }}
      <template v-slot:action>
        <q-btn flat color="white" label="Dismiss" @click="errorMessage = null" />
      </template>
    </q-banner>

    <q-input
      v-model="form.titulo"
      label="Title"
      :rules="[val => !!val || 'Title is required']"
      outlined
    />

    <q-input
      v-model="form.descricao"
      label="Description"
      type="textarea"
      :rules="[val => !!val || 'Description is required']"
      outlined
    />

    <q-select
      v-model="form.status"
      :options="statusOptions"
      label="Status"
      outlined
    />

    <q-input
      v-model="form.data_vencimento"
      label="Due Date"
      type="date"
      :rules="[val => !!val || 'Due date is required']"
      outlined
    >
      <template v-slot:prepend>
        <q-icon name="event" />
      </template>
    </q-input>

    <div class="row justify-end q-mt-md">
      <q-btn
        label="Cancel"
        color="grey-7"
        class="q-mr-sm"
        @click="$emit('cancel')"
        flat
      />
      <q-btn
        :label="task ? 'Update' : 'Create'"
        type="submit"
        color="primary"
        :loading="loading"
      />
    </div>
  </q-form>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, toRaw } from 'vue';
import { Task, TaskCreate, TaskUpdate, TaskStatus } from '@/types';
import { useTasksStore } from '@/stores';

const tasksStore = useTasksStore();
const errorMessage = ref<string | null>(null);

const props = defineProps<{
  task?: Task| any;
  loading?: boolean;
}>();

const emit = defineEmits<{
  (e: 'submit', task: TaskCreate | TaskUpdate): void;
  (e: 'cancel'): void;
}>();

// Watch for errors in the tasks store
watch(() => tasksStore.error, (newError) => {
  errorMessage.value = newError;
});

const statusOptions = [
  { label: 'Pending', value: 'pending' },
  { label: 'In Progress', value: 'in_progress' },
  { label: 'Completed', value: 'completed' },
];

const form = ref<{
  titulo: string;
  descricao: string;
  status: TaskStatus;
  data_vencimento: string;
}>({
  titulo: '',
  descricao: '',
  status: 'pending',
  data_vencimento: new Date().toISOString().split('T')[0],
});

onMounted(() => {
  if (props.task) {
    form.value.titulo = props.task.titulo;
    form.value.descricao = props.task.descricao;
    form.value.status = props.task.status;
    // Format the date for the date input (YYYY-MM-DD)
    const date = new Date(props.task.data_vencimento);
    form.value.data_vencimento = date.toISOString().split('T')[0];
  }
});

function onSubmit() {
  emit('submit', {
    titulo: form.value.titulo,
    descricao: form.value.descricao,
    status: form.value.status.value || form.value.status,
    data_vencimento: new Date(form.value.data_vencimento).toISOString(),
  });
}
</script>
