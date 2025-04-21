<template>
  <q-page padding>
    <div class="text-center q-pa-md">
      <h1 class="text-h3 q-mb-md">Welcome to Club Equindim Task Manager</h1>
      <p class="text-h6 q-mb-xl">Organize your tasks efficiently and boost your productivity</p>
      
      <div class="row justify-center q-mt-lg">
        <q-btn
          color="primary"
          label="Go to Tasks"
          size="lg"
          to="/tasks"
          class="q-px-xl"
        />
      </div>
      
      <div class="row justify-center q-mt-xl">
        <div class="col-12 col-md-8">
          <div class="row q-col-gutter-md">
            <div class="col-12 col-md-4">
              <q-card class="feature-card">
                <q-card-section>
                  <q-icon name="task" size="4rem" color="primary" />
                  <h2 class="text-h5 q-mt-md">Task Management</h2>
                  <p>Create, edit, and organize your tasks with ease.</p>
                </q-card-section>
              </q-card>
            </div>
            
            <div class="col-12 col-md-4">
              <q-card class="feature-card">
                <q-card-section>
                  <q-icon name="drag_indicator" size="4rem" color="primary" />
                  <h2 class="text-h5 q-mt-md">Drag & Drop</h2>
                  <p>Move tasks between different status columns with simple drag and drop.</p>
                </q-card-section>
              </q-card>
            </div>
            
            <div class="col-12 col-md-4">
              <q-card class="feature-card">
                <q-card-section>
                  <q-icon name="devices" size="4rem" color="primary" />
                  <h2 class="text-h5 q-mt-md">Responsive Design</h2>
                  <p>Access your tasks from any device with our responsive interface.</p>
                </q-card-section>
              </q-card>
            </div>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
// Home view component
</script>

<style scoped>
.feature-card {
  height: 100%;
  text-align: center;
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}
</style>
