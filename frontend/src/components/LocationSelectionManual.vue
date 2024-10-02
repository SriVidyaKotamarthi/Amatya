<template>
  <v-container class="mt-5 text-center">
    <h2>Select Your City</h2>
    <br>
    <v-row>
      <v-col v-for="city in cities" :key="city" cols="12" md="3">
        <v-card 
          class="hoverable city-card" 
          @click="selectCity(city)" 
          :class="{ 'selected-city': selectedCity === city }"
          elevation="5"
        >
          <v-img :src="cityImages[city]" height="150"></v-img>
          <v-card-title>{{ city }}</v-card-title>
        </v-card>
      </v-col>
    </v-row>
    
    <v-container v-if="selectedCity">
      <v-row>
        <v-col cols="12">
          <h2>Selected City: {{ selectedCity }}</h2>
          <v-form>
            <v-text-field
              v-model="locality"
              label="Locality"
              placeholder="Start typing locality"
              @input="emitLocationData"
            ></v-text-field>
            <v-text-field
              v-model="area"
              label="Area"
              placeholder="Start typing area"
              @input="emitLocationData"
            ></v-text-field>
            <v-text-field
              v-model="society"
              label="Society"
              placeholder="Start typing society"
              @input="emitLocationData"
            ></v-text-field>
            <v-text-field
              v-model="building"
              label="Building"
              placeholder="Start typing building"
              @input="emitLocationData"
            ></v-text-field>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </v-container>
</template>

<script>
export default {
  name: 'LocationSelectionManual',
  data() {
    return {
      locality: null,
      area: null,
      society: null,
      building: null,
      cities: [
        "Delhi", "Bengaluru", "Mumbai", "Chennai", "Hyderabad",
        "Pune", "Kolkata", "Ahmedabad"
      ],
      cityImages: {
        Delhi: require('@/assets/Delhi.png'),
        Bengaluru: require('@/assets/Bengaluru.png'),
        Mumbai: require('@/assets/Mumbai.png'),
        Chennai: require('@/assets/Chennai.png'),
        Hyderabad: require('@/assets/Hyderabad.png'),
        Pune: require('@/assets/Pune.png'),
        Kolkata: require('@/assets/Kolkata.png'),
        Ahmedabad: require('@/assets/Ahmedabad.png'),
      },
      selectedCity: null,
    };
  },
  methods: {
    selectCity(city) {
      this.selectedCity = city;
      this.emitLocationData();  // Emit the data immediately after selecting the city
    },
    emitLocationData() {
      // Emit all the location-related data whenever there is a change
      const data = {
        city: this.selectedCity,
        locality: this.locality,
        area: this.area,
        society: this.society,
        building: this.building,
      };
      this.$emit('locationSelected', data);
    },
  },
};
</script>

<style scoped>
.v-btn {
  margin-top: 20px;
}
.city-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.city-card:hover {
  transform: scale(1.05);
}
.selected-city {
  transform: scale(1.05);
  box-shadow: 0 0 0 2px #1976D2, 0 4px 20px rgba(0,0,0,0.1) !important;
}
</style>