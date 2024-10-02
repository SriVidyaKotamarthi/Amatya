<template>
  <v-container class="results-display" fluid>
    <v-row justify="center">
      <v-col cols="12" md="12" lg="12">
        <v-card class="pa-4 elevation-3">
          <v-card-title class="headline">Amatya's Observations</v-card-title>
          <v-divider></v-divider>

          <!-- Pros and Cons Section -->
          <v-row v-if="pros.length || cons.length" class="pros-cons-section">
            <!-- Pros Column -->
            <v-col cols="12" md="6">
              <v-card outlined class="mb-4">
                <v-card-title class="text--primary">Pros</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list dense>
                    <v-list-item v-for="(pro, index) in pros" :key="index">
                      <v-list-item-icon>
                        <v-icon color="green">mdi-check-circle-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content v-html="formatItem(pro)"></v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>

            <!-- Cons Column -->
            <v-col cols="12" md="6">
              <v-card outlined class="mb-4">
                <v-card-title class="text--error">Cons</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list dense>
                    <v-list-item v-for="(con, index) in cons" :key="index">
                      <v-list-item-icon>
                        <v-icon color="red">mdi-alert-circle-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content v-html="formatItem(con)"></v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Investment Potential Section -->
          <v-row v-if="investmentPotential">
            <v-col cols="12">
              <v-card class="highlight-card mb-4" outlined>
                <v-card-title class="text--investment">Investment Potential</v-card-title>
                <v-divider></v-divider>
                <v-card-text>{{ investmentPotential }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Lifestyle Match Section -->
          <v-row v-if="lifestyleMatch">
            <v-col cols="12">
              <v-card class="highlight-card mb-4" outlined>
                <v-card-title class="text--lifestyle">Lifestyle Match</v-card-title>
                <v-divider></v-divider>
                <v-card-text>{{ lifestyleMatch }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Recommendation Section -->
          <v-row v-if="recommendation">
            <v-col cols="12">
              <v-card class="highlight-card mb-4" outlined>
                <v-card-title class="text--recommend">Amatya's Recommendation</v-card-title>
                <v-divider></v-divider>
                <v-card-text>{{ recommendation }}</v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Next Steps Section -->
          <v-row v-if="nextSteps.length">
            <v-col cols="12">
              <v-card class="highlight-card mb-4" outlined>
                <v-card-title class="text--next-steps">Three Actionable Next Steps</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list dense>
                    <v-list-item v-for="(step, index) in nextSteps" :key="index">
                      <v-list-item-icon>
                        <v-icon color="blue">mdi-arrow-right-circle-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content v-html="formatItem(step)"></v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- Critical Questions Section -->
          <v-row v-if="criticalQuestions.length">
            <v-col cols="12">
              <v-card class="highlight-card mb-4" outlined>
                <v-card-title class="text--questions">Critical Questions for the User</v-card-title>
                <v-divider></v-divider>
                <v-card-text>
                  <v-list dense>
                    <v-list-item v-for="(question, index) in criticalQuestions" :key="index">
                      <v-list-item-icon>
                        <v-icon color="purple">mdi-help-circle-outline</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>{{ question }}</v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>

          <!-- No results to display section -->
          <v-row v-else-if="!pros.length && !cons.length && !recommendation">
            <v-col cols="12">
              <v-alert type="info" dismissible>No results to display.</v-alert>
            </v-col>
          </v-row>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  props: {
    pros: {
      type: Array,
      default: () => [],
    },
    cons: {
      type: Array,
      default: () => [],
    },
    recommendation: {
      type: String,
      default: '',
    },
    investmentPotential: {
      type: String,
      default: '',
    },
    lifestyleMatch: {
      type: String,
      default: '',
    },
    nextSteps: {
      type: Array,
      default: () => [],
    },
    criticalQuestions: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    formatItem(item) {
      const cleanItem = item.replace(/\*\*/g, ''); // Remove **
      const parts = cleanItem.split(':');
      if (parts.length > 1) {
        return `<strong>${parts[0]}:</strong> ${parts.slice(1).join(':').trim()}`;
      }
      return cleanItem;
    },
  },
};
</script>

<style scoped>
.results-display {
  margin-top: 20px;
  max-width: 1500px;
}

.v-card-title {
  font-weight: bold;
}

.v-list-item-content {
  font-size: 16px;
  color: #555;
  line-height: 1.5;
}

.text--primary {
  color: #4caf50;
}

.text--error {
  color: #f44336;
}

.text--recommend {
  color: #1976d2;
}

.text--investment {
  color: #ff9800;
}

.text--lifestyle {
  color: #3f51b5;
}

.text--next-steps {
  color: #009688;
}

.text--questions {
  color: #9c27b0;
}

.highlight-card {
  background-color: #f0f9ff;
  border-left: 5px solid #2196f3;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.v-alert {
  font-size: 16px;
}
</style>