<script setup lang="ts">
const { data } = await useFetch('http://back:5000/')
console.log(data)
console.log(data.value)

</script>

<template>
  <div>
    <h1>Hello </h1>
    <NuxtRouteAnnouncer />
    <NuxtWelcome />

  </div>
</template>
