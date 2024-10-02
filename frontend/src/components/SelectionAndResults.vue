<template>
    <v-container>
    <!-- Small banner as header for the SelectionAndResults page -->
      <BannerHeader :isSmall="true" />
      <!-- Location Selection Component -->
      <location-selection
        v-if="selectedCity"
        :selectedCity="selectedCity"
        @locationSelected="handleLocationSelection"
      />
  
      <!-- Priority Selection Component -->
      <priority-selection
        v-if="locationData"
        :locationData="locationData"
        @prioritiesSubmitted="handlePrioritiesSubmission"
      />
  
      <!-- Back and Submit Buttons -->
      <v-row class="mt-4">
        <v-col>
          <v-btn color="secondary" @click="goBackToCitySelection">Back to City Selection</v-btn>
          <v-btn color="primary" @click="fetchProsAndCons" v-if="locationData && selectedPriorities.length > 0">
            Help Me Choose
          </v-btn>
        </v-col>
      </v-row>
  
      <!-- Decision Factors Section -->
      <v-row v-if="decisionFactors">
        <v-col cols="12">
          <h3>Decision Factors</h3>
          <div v-for="(factor, index) in decisionFactors" :key="index">
            <p><strong>{{ factor.title }}</strong>: {{ factor.description }}</p>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import PrioritySelection from '@/components/PrioritySelection.vue';
  import BannerHeader from '@/components/BannerHeader.vue';

  import axios from 'axios';
  
  export default {
    components: {
        // LocationSelectionManual,
        // LocationSelectionGmaps,
      PrioritySelection,
      BannerHeader,
    },
    data() {
      return {
        selectedCity: this.$route.params.city, // Assuming selectedCity is passed via router
        locationData: null,
        selectedPriorities: [],
        decisionFactors: null,
      };
    },
    methods: {
      handleLocationSelection(data) {
        this.locationData = data;
      },
      handlePrioritiesSubmission(prioritiesData) {
        this.selectedPriorities = prioritiesData.user_priorities;
      },
      goBackToCitySelection() {
        this.$router.push('/');
      },
      fetchProsAndCons() {
        const data = {
          city: this.selectedCity,
          locationData: this.locationData,
          priorities: this.selectedPriorities,
        };
  
        axios.post('http://localhost:8000/get_pros_and_cons/', data).then((response) => {
          this.decisionFactors = response.data.factors; // assuming the backend returns factors in a 'factors' key
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .v-btn {
    margin-right: 10px;
  }
  </style>
  