<template>
  <header class="bg-[var(--primary-color)] text-white py-4 px-20 flex justify-between items-center">
    <RouterLink to="/">
      <div class="text-xl font-bold text-white">BackOffice</div>
    </RouterLink>
  </header>
</template>

<script>
import { RouterLink } from 'vue-router'

export default {
  name: 'HeaderComponent',
  components: {
    RouterLink
  }
};
</script>

<style scoped></style>