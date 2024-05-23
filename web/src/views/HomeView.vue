<template>
  <main class="main-container flex flex-col w-full h-full items-center p-8">
    <CarTableComponent :vozidlaData="vozidlaData" @vozidla-updated="updateData" /> 
  </main>
</template>

<script>
import CarTableComponent from '@/components/CarTableComponent.vue'
import axios from 'redaxios'

const url = "http://127.0.0.1:5000";

export default {
  name: 'HomeView',
  components: {
    CarTableComponent
  },
  data() {
    return {
      vozidlaData: []
    }
  },
  mounted() {
    this.fetchVozidla()
  },
  methods: {
    async fetchVozidla() {
      try {
        const response = await axios.get(`${url}/vozidla/`)
        this.vozidlaData = response.data
      } catch (error) {
        console.error('Error fetching vehicles:', error)
      }
    },
    updateData(newData) {
      this.vozidlaData = [...newData];
    }
  }
};
</script>


<style scoped lang="scss"></style>
