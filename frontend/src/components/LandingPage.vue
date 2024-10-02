<template>
  <v-app>
    <BannerHeader :isSmall="false" />

    <v-container class="location-selector-content">
      <div class="location-select-container">
        <v-switch 
          v-model="manualEntry"
          :label="manualEntry ? 'Enter manually' : 'Select on Map'"
          :prepend-icon="manualEntry ? 'mdi-keyboard' : 'mdi-map-marker'"
          class="mb-6"
        ></v-switch>
      </div>

      <v-card class="location-card">
        <v-card-text>
          <LocationSelectionManual 
            v-if="manualEntry" 
            @locationSelected="handleLocationSelected" 
          />
          <LocationSelectionGmaps 
            v-else 
            @locationSelected="handleLocationSelected" 
          />
        </v-card-text>
      </v-card>
    </v-container>

    <v-container>
      <v-card class="A3" v-if="selectedCity || !manualEntry">
        <v-card-text>
          <PrioritySelection @prioritiesUpdated="handlePrioritiesUpdate" />
        </v-card-text>
      </v-card>
      <br>
    </v-container>

    <div class="B2" v-if="isLocationValid">
      <v-btn color="primary" class="special-button" elevation="2" @click="submitSelection">
          Consult Amatya
      </v-btn>
    </div>
    <br>

    <v-container v-if="apiResponseReceived">
      <ResultsDisplay
        v-if="resultsAvailable"
        :pros="pros"
        :cons="cons"
        :recommendation="recommendation"
        :investmentPotential="investmentPotential"
        :lifestyleMatch="lifestyleMatch"
        :nextSteps="nextSteps"
        :criticalQuestions="criticalQuestions"
      />
      <p v-else>No results to display.</p>
    </v-container>

    <v-container v-if="apiResponseReceived && resultsAvailable">
      <ChatBot 
      :city="selectedCity"
      :locationDetails="locationDetails"
      :userPriorities="userSelectedPriorities"
      />
    </v-container>

    <v-dialog v-model="isLoading" hide-overlay persistent width="300">
      <v-card class="loading-modal">
        <v-card-text class="d-flex justify-center">
          <img :src="loadingGif" alt="Loading..." class="loading-gif">
        </v-card-text>
        <v-card-text class="text-center">
          <p>Processing... Please wait.</p>
        </v-card-text>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import BannerHeader from '@/components/BannerHeader.vue';
import LocationSelectionManual from '@/components/LocationSelectionManual';
import LocationSelectionGmaps from '@/components/LocationSelectionGmaps';
import PrioritySelection from '@/components/PrioritySelection';
import ResultsDisplay from '@/components/ResultsDisplay.vue';
import ChatBot from '@/components/ChatBot.vue';
import { ref } from 'vue';
import axios from 'axios';

export default {
  components: {
    BannerHeader,
    LocationSelectionManual,
    LocationSelectionGmaps,
    PrioritySelection,
    ResultsDisplay,
    ChatBot,
  },
  setup() {
    const manualEntry = ref(true);
    const selectedCity = ref(null);
    const userSelectedPriorities = ref([]);
    const isLocationValid = ref(false);
    const locationDetails = ref({});

    const apiResponseReceived = ref(false);
    const resultsAvailable = ref(false);
    const pros = ref([]);
    const cons = ref([]);
    const recommendation = ref('');

    const investmentPotential = ref('');
    const lifestyleMatch = ref('');
    const nextSteps = ref([]);
    const criticalQuestions = ref([]);

    const isLoading = ref(false);
    const loadingGif = ref(require('@/assets/loading.gif'));

    const handleLocationSelected = (data) => {
      selectedCity.value = data.city;
      locationDetails.value = { ...data };
      isLocationValid.value = !!data.city;
      console.log(data);
    };

    const handlePrioritiesUpdate = (selectedPriorities) => {
      userSelectedPriorities.value = selectedPriorities;
    };

  const parseResponse = (responseString) => {
  if (!responseString || typeof responseString !== 'string') {
    console.error('Invalid response format:', responseString);
    return {};
  }

  const extractSection = (text, sectionTitle) => {
    const regex = new RegExp(`\\*\\*${sectionTitle}:\\*\\*([\\s\\S]*?)(?=\\n\\*\\*|$)`);
    const match = text.match(regex);
    if (match) {
      return match[1]
        .split('\n')
        .map(item => {
          const parts = item.split(':');
          if (parts.length > 1) {
            return `<strong>${parts[0]}:</strong>${parts.slice(1).join(':')}`.trim();
          }
          return item.trim();
        })
        .filter(Boolean);
    }
    return [];
  };

  const responseObject = {};

  responseObject.top5pros = extractSection(responseString, "Top 5 Pros");
  responseObject.top5cons = extractSection(responseString, "Top 5 Cons");
  responseObject.investmentpotential = extractSection(responseString, "Investment Potential").join('');
  responseObject.lifestylematch = extractSection(responseString, "Lifestyle Match").join('');
  responseObject.overallrecommendation = extractSection(responseString, "Overall Recommendation").join('');
  responseObject.threeactionablenextsteps = extractSection(responseString, "Three Actionable Next Steps");
  responseObject.criticalquestionsfortheuser = extractSection(responseString, "Critical Questions for the User");

  return responseObject;
};

    const submitSelection = async () => {
      const payload = {
        city: selectedCity.value,
        locality: locationDetails.value.locality || '',
        area: locationDetails.value.area || '',
        society: locationDetails.value.society || '',
        building: locationDetails.value.building || '',
        address: locationDetails.value.address || '',
        user_priorities: userSelectedPriorities.value || {}
      };

      console.log("Address given is: ");
      console.log(locationDetails.value.address);

      isLoading.value = true;

      try {
         const response = await axios.post('/api/genaitool/get_ai_response/', payload);

        if (response.data && response.data.response) {
          const parsedResponse = parseResponse(response.data.response);
          console.log("****************")
          console.log(parseResponse)
          console.log(response.data.response)
          pros.value = parsedResponse.top5pros || [];
          cons.value = parsedResponse.top5cons || [];
          console.log('Pros:' , pros.value)
          console.log('Cons:', cons.value)
          recommendation.value = parsedResponse.overallrecommendation || '';
          investmentPotential.value = parsedResponse.investmentpotential || '';
          lifestyleMatch.value = parsedResponse.lifestylematch || '';
          nextSteps.value = parsedResponse.threeactionablenextsteps || [];
          criticalQuestions.value = parsedResponse.criticalquestionsfortheuser || [];

          resultsAvailable.value = Object.keys(parsedResponse).length > 0;
        } else {
          resultsAvailable.value = false;
        }
        apiResponseReceived.value = true;
      } catch (error) {
        console.error('Error submitting selection:', error);
        apiResponseReceived.value = true;
        resultsAvailable.value = false;
      } finally {
        isLoading.value = false;
      }
    };

    return {
      manualEntry,
      selectedCity,
      handleLocationSelected,
      handlePrioritiesUpdate,
      submitSelection,
      isLocationValid,
      apiResponseReceived,
      resultsAvailable,
      pros,
      cons,
      recommendation,
      investmentPotential,
      lifestyleMatch,
      nextSteps,
      criticalQuestions,
      isLoading,
      loadingGif,
    };
  },
};
</script>

<style scoped>
.B2 {
  display: flex;
  justify-content: center;
  align-items: center;
}

.special-button {
  font-size: 16px;
  padding: 12px 24px;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.special-button:hover {
  background-color: #0056b3;
}

.loading-modal {
  text-align: center;
  padding: 20px;
}

.loading-gif {
  width: 100px;
}
</style>