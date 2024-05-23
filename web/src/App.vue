<template>
  <div class="w-full h-full flex flex-col">
    <Notifications position="bottom right" />
    <HeaderComponent />
    <RouterView />
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue';

export default {
  name: 'App',
  components: {
    HeaderComponent,
    RouterView
  },

}
</script>

<style scoped lang="scss"></style>
