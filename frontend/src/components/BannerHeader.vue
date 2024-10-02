<template>
    <div :class="['banner', isSmall ? 'banner-small' : 'banner-large']">
      <v-container>
        <v-row class="justify-center">
          <v-col cols="12" class="text-center">
            <!-- Logo Icon -->
            <v-img
              src="@/assets/logo.png"
              alt="Amatya Logo"
              :max-width="isSmall ? 60 : 120"
              class="mx-auto"
            ></v-img>
            <!-- Main Title -->
            <h1 class="main-title">Amatya</h1>
            <!-- Subtitle -->
            <h2 class="sub-title">Your Expert Advisor</h2>
            <!-- Tag Line -->
            <h3 class="tag-line">I help you choose the right place to live</h3>
          </v-col>
        </v-row>
      </v-container>
    </div>
  </template>
  
  <script>
  export default {
    name: 'BannerHeader',
    props: {
      isSmall: {
        type: Boolean,
        default: false,
      },
    },
  };
  </script>
  
  <style scoped>
  /* General banner styles */
  .banner {
    background: linear-gradient(
        rgba(0, 0, 255, 0.7),
        rgba(0, 128, 255, 0.3)
      ), 
      url('@/assets/background-image.png');
    background-size: cover;
    background-position: center;
    color: white;
    text-align: center;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  /* Large banner for landing page */
  .banner-large {
    height: 400px;
    border-bottom: 5px solid rgba(0, 0, 255, 0.4);
  }
  
  /* Small banner for other pages */
  .banner-small {
    height: 170px;
    border-bottom: 2px solid rgba(0, 0, 255, 0.4);
  }
  
  /* Styling for main title, subtitle, and tagline */
  .main-title {
    font-size: 3.5rem;
    font-weight: bold;
    margin: 0;
    color: white;
    text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
  }
  
  .sub-title {
    font-size: 1.5rem;
    margin: 10px 0;
    font-weight: 400;
    color: white;
    text-shadow: 2px 2px 7px rgba(0, 0, 0, 0.8);
  }
  
  .tag-line {
    font-size: 1.2rem;
    font-weight: 500;
    color: white;
    text-shadow: 2px 2px 7px rgba(0, 0, 0, 0.8);
  }
  
  /* Adjustments for smaller banner */
  .banner-small .main-title {
    font-size: 2rem;
  }
  
  .banner-small .sub-title {
    font-size: 1rem;
  }
  
  .banner-small .tag-line {
    font-size: 0.9rem;
  }
  
  /* Responsive design */
  @media (max-width: 600px) {
    .main-title {
      font-size: 2.5rem;
    }
  
    .sub-title {
      font-size: 1.2rem;
    }
  
    .tag-line {
      font-size: 1.5rem;
    }
  
    .banner-small .main-title {
      font-size: 1.5rem;
    }
  
    .banner-small .sub-title {
      font-size: 0.9rem;
    }
  
    .banner-small .tag-line {
      font-size: 0.75rem;
    }
  }
  </style>
  