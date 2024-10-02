<template>
    <v-container fluid class="priority-selection-container">
      <h2 class="text-center mb-6">Select Your Priorities</h2>
      <v-row justify="center">
        <v-col
          v-for="(priority, index) in displayedPriorities"
          :key="index"
          cols="12"
          sm="6"
          md="4"
          lg="3"
          xl="2"
        >
          <v-card
            class="mx-auto priority-card"
            :class="{ selected: isSelected(priority.name) }"
            @click="togglePriority(priority.name)"
          >
            <v-card-text class="text-center">
              <template v-if="priority.name === 'Cultural Centers'">
                <div class="icon-wrapper">
                  <v-img
                    :src="require('@/assets/cultural.png')"
                    width="48"
                    height="48"
                    contain
                  ></v-img>
                </div>
              </template>
              <template v-else>
                <v-icon size="48" class="mb-2">{{ priority.icon }}</v-icon>
              </template>
              <h3 class="priority-title">{{ priority.name }}</h3>
              <p class="priority-description">{{ priority.description }}</p>
            </v-card-text>
            <div v-if="isSelected(priority.name)" class="rank-circle">
              {{ getRank(priority.name) }}
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    name: 'PrioritySelection',
    props: ['locationData'],
    data() {
      return {
        displayedPriorities: [
          { name: "Basic Infrastructure", description: "Essential services", icon: "mdi-home-city" },
          { name: "Legal & Safety", description: "Security and protection", icon: "mdi-shield-check" },
          { name: "Environmental Factors", description: "Air quality and green spaces", icon: "mdi-nature" },
          { name: "Connectivity", description: "Transportation and networks", icon: "mdi-bus-clock" },
          { name: "Social Amenities", description: "Schools and hospitals", icon: "mdi-hospital-building" },
          { name: "Community", description: "Local culture and activities", icon: "mdi-account-group" },
          { name: "Economic Factors", description: "Cost of living and jobs", icon: "mdi-currency-usd" },
          { name: "Urban Planning", description: "City layout and development", icon: "mdi-city" },
          { name: "Technology", description: "Internet and smart initiatives", icon: "mdi-wifi" },
          { name: "Climate", description: "Weather patterns", icon: "mdi-weather-partly-cloudy" },
          { name: "Pet-friendliness", description: "Services for pets", icon: "mdi-paw" },
          { name: "Cultural Centers", description: "Worship and cultural spots", icon: "cultural" }, // Placeholder
          { name: "Workspaces", description: "Offices and co-working", icon: "mdi-desktop-mac-dashboard" },
          { name: "Public Spaces", description: "Parks and recreation", icon: "mdi-tree" }
        ].sort(() => Math.random() - 0.5),
        selectedPriorities: [],
      };
    },
    methods: {
      togglePriority(priority) {
        const index = this.selectedPriorities.indexOf(priority);
        if (index > -1) {
          this.selectedPriorities.splice(index, 1);
        } else {
          this.selectedPriorities.push(priority);
        }
        this.$emit('prioritiesUpdated', this.selectedPriorities); // Emit updated priorities
      },
      isSelected(priority) {
        return this.selectedPriorities.includes(priority);
      },
      getRank(priority) {
        return this.selectedPriorities.indexOf(priority) + 1;
      },
    },
  };
  </script>
  
  <style scoped>
  .priority-selection-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    padding: 2rem;
  }
  
  .priority-card {
    height: 100%;
    transition: all 0.3s;
    border-radius: 15px;
    overflow: hidden;
    background: white;
    position: relative;
  }
  
  .priority-card.selected {
    border: 2px solid #4facfe;
  }
  
  .priority-title {
    font-size: 1.2rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
  }
  
  .priority-description {
    font-size: 0.9rem;
    opacity: 0.8;
  }
  
  .rank-circle {
    position: absolute;
    top: 5px;
    right: 5px;
    width: 30px;
    height: 30px;
    border-radius: 50%;
    background-color: #4facfe;
    color: white;
    display: flex;
    justify-content: center;
    align-items: center;
    font-weight: bold;
    font-size: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }
  
  .icon-wrapper {
    display: flex;
    justify-content: center; /* Center the icon horizontally */
    align-items: center;   /* Center the icon vertically */
    height: 48px;         /* Set height to match the icon size */
  }
  </style>