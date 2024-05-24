<template>
  <div class="flex items-center content-center flex-col py-4 px-20 space-y-6">
    <div class="flex flex-col items-center justify-center space-y-6" v-if="isEditing">
      <h3 class="text-lg font-bold">Upraviť Vozidlo</h3>
      <div class="flex flex-1 items-center justify-center space-x-2">
        <FloatLabel class="w-full">
          <InputText id="kategoria" v-model="selectedVozidlo.Kategoria_vozidla" />
          <label for="kategoria">Kategoria</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <InputText id="znacka" v-model="selectedVozidlo.Znacka_vozidla" />
          <label for="znacka">Znacka</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <InputNumber inputId="integeronly" id="cena" v-model="selectedVozidlo.Predajna_cena" />
          <label for="cena">Predajna Cena</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <Calendar id="datum" v-model="selectedVozidlo.Datum_vytvorenia" dateFormat="yy-mm-dd" />
          <label for="datum">Datum Vytvorenia</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <InputText id="stav" v-model="selectedVozidlo.Stav" />
          <label for="stav">Stav</label>
        </FloatLabel>
      </div>
      <div class="flex flex-1 items-center justify-center space-x-4">
        <ButtonPrime @click="updateVozidlo">Aktualizovať</ButtonPrime>
        <ButtonPrime class="p-button-danger" @click="cancelEdit">Zrušiť</ButtonPrime>
      </div>
    </div>

    <div class="flex flex-col items-center justify-center space-y-6" v-else>
      <h3 class="text-lg font-bold">Pridať nové Vozidlo</h3>
      <div class="flex flex-1 items-center justify-center space-x-2">
        <FloatLabel class="w-full">
          <InputText id="kategoria" v-model="newVozidlo.Kategoria_vozidla" />
          <label for="kategoria">Kategoria</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <InputText id="znacka" v-model="newVozidlo.Znacka_vozidla" />
          <label for="znacka">Znacka</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <InputText id="cena" v-model="newVozidlo.Predajna_cena" />
          <label for="cena">Predajna Cena</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <Calendar id="datum" v-model="newVozidlo.Datum_vytvorenia" dateFormat="dd-mm-yy" />
          <label for="datum">Datum Vytvorenia</label>
        </FloatLabel>
        <FloatLabel class="w-full">
          <InputText id="stav" v-model="newVozidlo.Stav" />
          <label for="stav">Stav</label>
        </FloatLabel>
      </div>
      <ButtonPrime @click="addVozidlo">Pridať</ButtonPrime>
    </div>

    <DataTable :value="vozidlaData" v-if="vozidlaData.length > 0 && !isLoading">
      <Column field="Kategoria_vozidla" header="Kategoria"></Column>
      <Column field="Znacka_vozidla" header="Znacka"></Column>
      <Column field="Predajna_cena" header="Predajna Cena"></Column>
      <Column field="Datum_vytvorenia" header="Datum Vytvorenia"></Column>
      <Column field="Stav" header="Stav"></Column>
      <Column>
        <template #body="slotProps">
          <div class="flex flex-1 items-center justify-center space-x-2">
            <ButtonPrime 
              @click="editVozidlo(slotProps.data)" 
              icon="pi pi-pen-to-square" 
              :disabled="isEditing"
            />
            <ButtonPrime 
              class="p-button-danger" 
              @click="deleteVozidlo(slotProps.data)" 
              icon="pi pi-trash" 
              :disabled="isEditing" 
            />
          </div>
        </template>         
      </Column>
    </DataTable>
    <ProgressSpinner v-else-if="isLoading" style="width: 50px; height: 50px" strokeWidth="8" fill="var(--surface-ground)" animationDuration=".5s" aria-label="Custom ProgressSpinner" />
  </div>
</template>


<script>
import axios from 'redaxios'
import ButtonPrime from 'primevue/button'
import FloatLabel from 'primevue/floatlabel'
import InputText  from 'primevue/inputtext'
import Column from 'primevue/column'
import DataTable from 'primevue/datatable'
import Calendar from 'primevue/calendar'
import InputNumber from 'primevue/inputnumber'
import ProgressSpinner from 'primevue/progressspinner';

const url = "http://127.0.0.1:5000";

export default {
  name: 'CarTableComponent',
  components: {
    ButtonPrime,
    FloatLabel,
    InputText,
    Column,
    DataTable,
    Calendar,
    InputNumber,
    ProgressSpinner
  },
  data() {
    return {
      isEditing: false,
      isLoading: false,
      selectedVozidlo: {},
      newVozidlo: {
        Kategoria_vozidla: '',
        Znacka_vozidla: '',
        Predajna_cena: null,
        Datum_vytvorenia: '',
        Stav: ''
      },
      vozidlaData: [],
      categories: [
        {name: "PKW"},
        {name: "LKW"}
      ],
      columns: [
        { field: 'Kategoria_vozidla', header: 'Kategória' },
        { field: 'Znacka_vozidla', header: 'Značka' },
        { field: 'Predajna_cena', header: 'Predajná Cena' },
        { field: 'Datum_vytvorenia', header: 'Dátum Vytvorenia' },
        { field: 'Stav', header: 'Stav' }
      ]
    }
  },
  mounted() {
    this.fetchVozidla()
  },
  methods: {
    async fetchVozidla() {
      this.isLoading = true; 
      try {
        const response = await axios.get(`${url}/vozidla/`)
        this.vozidlaData = response.data
        this.isLoading = false;
      } catch (error) {
        console.error('Error fetching vehicles:', error)
      }
    },
    async addVozidlo() {
        // Validate new vehicle data
        let errorMessage = "";

        if (!this.newVozidlo.Kategoria_vozidla) {
          errorMessage += "Please enter a category for the new vehicle. \n";
        }

        if (!this.newVozidlo.Znacka_vozidla) {
          errorMessage += "Please enter a brand for the new vehicle. \n";
        }

        // Minimum length validation
        if (this.newVozidlo.Kategoria_vozidla && this.newVozidlo.Kategoria_vozidla.length < 3) {
          errorMessage += "Category must be at least 3 characters long. \n";
        }

        // Date validation 
        if (!this.newVozidlo.Datum_vytvorenia) {
          errorMessage += "Please enter a valid creation date. \n";
        }

        // Price validation
        if (this.newVozidlo.Predajna_cena && this.newVozidlo.Predajna_cena < 0) {
          errorMessage += "Predajna Cena cannot be negative. \n";
        }

        // Check for duplicate brand before creating new vehicle
        const brandToCheck = this.newVozidlo.Znacka_vozidla.trim().toUpperCase();
        const existingVehicle = this.vozidlaData.find(v => v.Znacka_vozidla.trim().toUpperCase() === brandToCheck);
        if (existingVehicle) {
          errorMessage += "A vehicle with this brand already exists. \n";
        }
        
        if (errorMessage) {
          this.$notify({
            type: "error",
            title: 'Validation Error',
            text: errorMessage
          });
          return; 
        }

      try {
        const response = await axios({
          method: "post",
          url: `${url}/vozidla/`,
          data: this.newVozidlo,
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
          }
        })
        this.vozidlaData.push(response.data) // Add new vehicle to local data
        this.$emit('vozidla-updated', this.vozidlaData.slice()) // Emit event with a copy
        this.newVozidlo = { // Reset new vehicle data
          Kategoria_vozidla: '',
          Znacka_vozidla: '',
          Predajna_cena: null,
          Datum_vytvorenia: '',
          Stav: ''
        }
      } catch (error) {
        console.error('Error adding vehicle:', error)
      }
    },
    editVozidlo(vozidlo) {
      this.isEditing = true
      this.selectedVozidlo = { ...vozidlo } // Create a copy
    },
    cancelEdit() {
      this.isEditing = false
      this.selectedVozidlo = null
    },
    async updateVozidlo() {
      try {
        const response = await axios({
          method: "put",
          url: `${url}/vozidla/${this.selectedVozidlo.id}`,
          data: this.selectedVozidlo
        })
        const updatedIndex = this.vozidlaData.findIndex(v => v.id === response.data.id)
        if (updatedIndex !== -1) {
          this.vozidlaData.splice(updatedIndex, 1, response.data) // Update local data
          this.$emit('vozidla-updated', this.vozidlaData.slice()) // Emit event with a copy
        }
        this.isEditing = false
        this.selectedVozidlo = {}
      } catch (error) {
        console.error('Error updating vehicle:', error)
      }
    },
    async deleteVozidlo(vozidlo) {
      try {
        await axios.delete(`${url}/vozidla/${vozidlo.id}`)
        const deletedIndex = this.vozidlaData.findIndex(v => v.id === vozidlo.id)
        if (deletedIndex !== -1) {
          this.vozidlaData.splice(deletedIndex, 1)
          this.$emit('vozidla-updated', this.vozidlaData.slice()) //
        }
      } catch (error) {
        console.error('Error deleting vehicle:', error)
      }
    }
  }
};
</script>

