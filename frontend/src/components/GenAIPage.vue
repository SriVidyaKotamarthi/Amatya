<template>
  <div class="page-genaiquerytool">
    <!-- Heading of the Page -->
    <div class="columns is-multiline">
      <div class="column is-12">
          <h1 class="title" style="text-align: center;">AI-Based Tool</h1>
      </div>
    </div>
    
    <wb-input as="textarea" autoComplete autoFocus= "true"
      placeholder="Please input your Prompt here" 
      v-model="userPrompt">
      <span>Enter your query</span>
      <wb-control-hint>For accurate results please be specific in your propmt</wb-control-hint>
    </wb-input>
    <div class="center">
      <wb-button class="item3" theme="light" variant="primary" id="generatesql" 
      :disabled="disableGenerate" size="s" @click="getResponse">
        <wb-icon flip-rtl name="bds/open-new/24"></wb-icon>Generate Response
      </wb-button>
    </div>
    <div>
    <div v-if="showResults">
      <div :hidden=!showResults>
          <!-- <wb-heading size="xs" :hidden=!showResults>{{ key }}</wb-heading> -->
          <br>
          <wb-input as="textarea" :value=resp.response readonly :hidden=!showResults autoGrow>
          </wb-input>
            <br>
      </div>
      </div>
      </div>
  </div>
</template>

<script>
import axios from 'axios';
import { WbInput, WbIcon } from '@workbench/vue';


export default {
  name: "GenAIPage",
  components: {
  WbIcon,
  WbInput,
  },
  data() {
    return {
      userPrompt: '',
      queryObj: {},
      showResults: false,
      disableGenerate: false,
      disableRun: true,
      csrfToken: '',
      errors:[],
      resp:{}
    };
  },
  methods: {
    async getResponse() {
      if (this.userPrompt != '') {
        this.showResults = false
        try {
          const csrfToken = this.csrfToken;
          const headers = {
          "Content-Type": "application/json", // Set the content type
          "X-CSRFToken": csrfToken,
          //  "cache": no-cache,
          };
          const axiosConfig = {
            headers,
            withCredentials: true,
          };
          // Replace with the actual endpoint URL
          const response = await axios.post('/api/genaitool/get_ai_response', 
            { userprompt: this.userPrompt },axiosConfig);
          
          if (response.status !== 200) {
            throw new Error(`HTTP error: ${response.status}`);
          }
          // Check for backend errors
          if (response.data.error) {
            throw new Error(response.data.error);
            }
          this.resp = response.data;
          console.log(this.resp)
          this.disableRun = false;
          this.showResults = true;
          this.showModal = false;
        } catch (error) {
      const genericErrorMessage =
           "There is some issue in processing your request. Please check your request and retry.";
      // Check if the generic error message is not already in the errors array
      if (!this.errors.includes(genericErrorMessage)) {
        this.errors.push(genericErrorMessage);
        this.errors.push("Error in Fetching submit Request", error);
        this.showError = true;
        this.showModal = false;
      } else {
        this.errors.push("Error in Fetching submit Request", error);
        this.showError = true;
        this.showModal = false;
      }
    }
      }
      else {
        this.showErrorHint = true
    }
    },

   closeModal() {
    this.showError = false;
    this.errors = [];
  },
  },
};
</script>

<style>
.disclaimer {
  color: red;
  font-size: 0.8em;
}

.center {
text-align: center;
}

.item3 {
width: 25%;
margin-right: 10px; /* Adjust the spacing as needed */
}

.gif {
width: 50px !important; /* Make sure the GIF doesn't exceed the width of the modal content */
height: "auto" !important; /* Set the maximum height for the GIF */
margin: 0 auto; /* Center horizontally */
}

.model {
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
display: flex;
align-items: center;
justify-content: center;
}

.model-image {
max-width: 100%;
max-height: 100%;
width: 50px;
height: 50px;
display: block;
margin-left: auto;
margin-right: auto;
}

.model-content {
background-color: white;
padding: 20px;
text-align: center;
border-radius: 10px;
display: flex;
flex-direction: column;
width: 60%;
/* box-sizing: border-box; */
}

.ok {
cursor: pointer;
background-color: red;
color: white;
padding: 5px 1px;
border-radius: 10px;
}
/* Add more styles as needed */
</style>