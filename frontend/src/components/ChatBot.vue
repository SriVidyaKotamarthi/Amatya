<template>
  <v-container class="chatbot-container">
    <v-card outlined>
      <v-card-title class="headline">Ask Amatya’s Wisdom</v-card-title>
      <v-divider></v-divider>
      <v-card-text>
        <div v-if="conversation.length > 0">
          <div v-for="(message, index) in conversation" :key="index" class="chat-message">
            <div v-if="message.type === 'user'" class="user-message">
              <strong>You:</strong> {{ message.text }}
            </div>
            <div v-else class="bot-message">
              <strong>Bot:</strong> {{ message.text }} <br />
              <em v-if="message.category">Category: {{ message.category }}</em>
              <em v-else>{{ message.loadingText }}</em>
            </div>
            <v-divider></v-divider>
          </div>
        </div>

        <v-textarea
          v-model="userPrompt"
          label="Ask a question about the locality"
          rows="3"
          auto-grow
        ></v-textarea>
        <v-btn 
          color="primary" 
          @click="submitPrompt"
          :disabled="isLoading || !userPrompt.trim()"
        >
          Ask
        </v-btn>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    city: String,
    locationDetails: Object,
    userPriorities: Array,
  },
  data() {
    return {
      userPrompt: '',
      conversation: [],
      isLoading: false,
    };
  },
  methods: {
    async submitPrompt() {
      if (!this.userPrompt.trim()) return;

      this.conversation.push({ type: 'user', text: this.userPrompt });

      const prompt = this.userPrompt;
      this.userPrompt = '';
      this.isLoading = true;

      try {
        const classifyResponse = await axios.post('/api/chatbot/classify/', { question: prompt });

        const { classified_category, agent } = classifyResponse.data;

        this.conversation.push({
          type: 'bot',
          text: '',
          category: null,
          loadingText: `Checking with ${agent}...`,
        });

        const response = await axios.post('/api/chatbot/generate-response/', {
          category: classified_category,
          question: prompt,
          city: this.city,
          locationDetails: this.locationDetails,
          userPriorities: this.userPriorities,
        });

        this.conversation.pop();
        this.conversation.push({
          type: 'bot',
          text: response.data.response,
          category: classified_category,
        });
      } catch (error) {
        console.error('Error getting response:', error);
        this.conversation.push({
          type: 'bot',
          text: 'Sorry, something went wrong while fetching the expert response.',
          category: null,
        });
      } finally {
        this.isLoading = false;
      }
    },
  },
};
</script>

<style scoped>
.chatbot-container {
  margin-top: 20px;
}

.chat-message {
  margin-bottom: 10px;
}

.user-message {
  background-color: #e3f2fd;
  padding: 10px;
  border-radius: 5px;
}

.bot-message {
  background-color: #f1f8e9;
  padding: 10px;
  border-radius: 5px;
}
</style>