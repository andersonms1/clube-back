<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <div v-if="error" class="text-negative q-mb-md">
      {{ error }}
    </div>

    <q-input
      v-model="form.email"
      label="Email"
      type="email"
      :rules="[
        val => !!val || 'Email is required',
        val => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(val) || 'Please enter a valid email'
      ]"
      outlined
    >
      <template v-slot:prepend>
        <q-icon name="email" />
      </template>
    </q-input>

    <q-input
      v-model="form.password"
      label="Password"
      :type="showPassword ? 'text' : 'password'"
      :rules="[val => !!val || 'Password is required']"
      outlined
    >
      <template v-slot:prepend>
        <q-icon name="lock" />
      </template>
      <template v-slot:append>
        <q-icon
          :name="showPassword ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="showPassword = !showPassword"
        />
      </template>
    </q-input>

    <div class="row justify-between items-center q-mt-sm">
      <q-checkbox v-model="rememberMe" label="Remember me" />
      <q-btn
        flat
        color="primary"
        label="Forgot password?"
        @click="$emit('forgot-password')"
        no-caps
      />
    </div>

    <div class="row justify-center q-mt-lg">
      <q-btn
        type="submit"
        color="primary"
        :loading="loading"
        size="lg"
        class="full-width"
        label="Login"
      />
    </div>

    <div class="row justify-center q-mt-md">
      <p class="text-grey-7">
        Don't have an account?
        <q-btn
          flat
          color="primary"
          label="Register"
          @click="$emit('register')"
          no-caps
          padding="xs"
        />
      </p>
    </div>
  </q-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UserCredentials } from '@/types';


const {loading, error} = defineProps<{
  loading?: boolean;
  error?: string | null;
}>();

const emit = defineEmits<{
  (e: 'submit', credentials: UserCredentials): void;
  (e: 'forgot-password'): void;
  (e: 'register'): void;
}>();

const form = ref<UserCredentials>({
  email: '',
  password: '',
});

const showPassword = ref(false);
const rememberMe = ref(false);

function onSubmit() {
  emit('submit', form.value);
}
</script>
