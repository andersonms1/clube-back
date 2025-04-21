<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <div v-if="error" class="text-negative q-mb-md">
      {{ error }}
    </div>

    <q-input
      v-model="form.username"
      label="Username"
      :rules="[val => !!val || 'Username is required']"
      outlined
    >
      <template v-slot:prepend>
        <q-icon name="person" />
      </template>
    </q-input>

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
      :rules="[
        val => !!val || 'Password is required',
        val => val.length >= 8 || 'Password must be at least 8 characters'
      ]"
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

    <q-input
      v-model="confirmPassword"
      label="Confirm Password"
      :type="showConfirmPassword ? 'text' : 'password'"
      :rules="[
        val => !!val || 'Please confirm your password',
        val => val === form.password || 'Passwords do not match'
      ]"
      outlined
    >
      <template v-slot:prepend>
        <q-icon name="lock" />
      </template>
      <template v-slot:append>
        <q-icon
          :name="showConfirmPassword ? 'visibility_off' : 'visibility'"
          class="cursor-pointer"
          @click="showConfirmPassword = !showConfirmPassword"
        />
      </template>
    </q-input>

    <div class="row justify-center q-mt-lg">
      <q-btn
        type="submit"
        color="primary"
        :loading="loading"
        size="lg"
        class="full-width"
        label="Register"
      />
    </div>

    <div class="row justify-center q-mt-md">
      <p class="text-grey-7">
        Already have an account?
        <q-btn
          flat
          color="primary"
          label="Login"
          @click="$emit('login')"
          no-caps
          padding="xs"
        />
      </p>
    </div>
  </q-form>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { UserRegistration } from '@/types';

const { loading, error } = defineProps<{
  loading?: boolean;
  error?: string | null;
}>();

const emit = defineEmits<{
  (e: 'submit', userData: UserRegistration): void;
  (e: 'login'): void;
}>();

const form = ref<UserRegistration>({
  username: '',
  email: '',
  password: '',
});

const confirmPassword = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

function onSubmit() {
  emit('submit', form.value);
}
</script>
