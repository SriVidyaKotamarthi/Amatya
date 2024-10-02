<template>
  <v-row>
    <v-col v-for="city in cities" :key="city" cols="12" md="3">
      <v-card class="hoverable" @click="$emit('city-selected', city)" elevation="5">
        <v-img :src="cityImages[city]" height="150"></v-img>
        <v-card-title>{{ city }}</v-card-title>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  data() {
    return {
      cities: ["Delhi", "Bengaluru", "Mumbai", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"],
      cityImages: {
        Delhi: require('@/assets/Delhi.png'),
        Bengaluru: require('@/assets/Bengaluru.png'),
        Mumbai: require('@/assets/Mumbai.png'),
        Chennai: require('@/assets/Chennai.png'),
        Hyderabad: require('@/assets/Hyderabad.png'),
        Pune: require('@/assets/Pune.png'),
        Kolkata: require('@/assets/Kolkata.png'),
        Ahmedabad: require('@/assets/Ahmedabad.png'),
      }
    };
  }
};
</script>
