<template>
  <q-form @submit="onSubmit" class="q-gutter-md">
    <div v-if="error" class="text-negative q-mb-md">
      {{ error }}
    </div>

    <div v-if="!token">
      <p class="text-center q-mb-lg">
        Enter your email address and we'll send you a link to reset your password.
      </p>

      <q-input
        v-model="email"
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
    </div>

    <div v-else>
      <p class="text-center q-mb-lg">
        Enter your new password below.
      </p>

      <q-input
        v-model="password"
        label="New Password"
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
          val => val === password || 'Passwords do not match'
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
    </div>

    <div class="row justify-center q-mt-lg">
      <q-btn
        type="submit"
        color="primary"
        :loading="loading"
        size="lg"
        class="full-width"
        :label="token ? 'Reset Password' : 'Send Reset Link'"
      />
    </div>

    <div class="row justify-center q-mt-md">
      <p class="text-grey-7">
        Remember your password?
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

const props = defineProps<{
  token?: string;
  loading?: boolean;
  error?: string | null;
}>();

const emit = defineEmits<{
  (e: 'submit-email', email: string): void;
  (e: 'submit-password', password: string): void;
  (e: 'login'): void;
}>();

const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const showPassword = ref(false);
const showConfirmPassword = ref(false);

function onSubmit() {
  if (props.token) {
    emit('submit-password', password.value);
  } else {
    emit('submit-email', email.value);
  }
}
</script>
