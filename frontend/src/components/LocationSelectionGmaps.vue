<template>
    <v-container class="location-selection-container">
      <!-- <v-row>
        <v-col cols="12">
           Section Heading 
          <div class="header-section">
            <v-img
              src="@/assets/logo.png"
              alt="Amatya Logo"
              max-width="60"
              class="mx-auto"
            />
            <h1 class="header-title">Amatya</h1>
            <h2 class="header-subtitle">Your Expert Advisor</h2>
            <h3 class="header-tagline">I help you choose the right place to live</h3>
          </div>
        </v-col>
      </v-row> -->
  
      <v-row>
      <v-col cols="12">
        <!-- Location Selection Section -->
        <h2 class="section-title">Select Your Location</h2>
        <v-form>
          <v-text-field
            v-model="address"
            label="Enter Address"
            ref="autocomplete"
            placeholder="Start typing your address"
            solo
            hide-details
            class="location-input"
          />
        </v-form>
      </v-col>
    </v-row>
  
      <v-row>
        <v-col cols="12">
          <!-- Map Display -->
          <GMapMap
            :center="center"
            :zoom="12"
            style="height: 400px; width: 100%;"
            class="map-container"
            @click="updateMapLocation"
          >
            <GMapMarker :position="center" />
          </GMapMap>
        </v-col>
      </v-row>
  
      <!-- Button to trigger priority selection and fetch external data
      <v-row>
        <v-col cols="12">
          <v-btn @click="fetchAirQualityAndPollen" class="check-btn">
            Check Air Quality and Pollen
          </v-btn>
        </v-col>
      </v-row> -->
  
      <!-- Display Air Quality and Pollen Information
      <v-row v-if="airQuality || pollenInfo">
        <v-col cols="12" class="info-section">
          <h3 v-if="airQuality">Air Quality: {{ airQuality }}</h3>
          <h3 v-if="pollenInfo">Pollen Info: {{ pollenInfo }}</h3>
        </v-col>
      </v-row> -->
  
      <!-- Proceed to Priority Selection
      <v-row>
        <v-col cols="12">
          <v-btn @click="goToPriorities" class="next-btn">Next: Set Priorities</v-btn>
        </v-col>
      </v-row> -->
    </v-container>
  </template>
  
  <script>
  /* global google */  // This informs ESLint that 'google' is a global object

  export default {
    name: 'LocationSelectionGmaps',
    data() {
      return {
        address: '',
        center: { lat: -34.397, lng: 150.644 }, // Default location
        airQuality: null,
        pollenInfo: null,
        city: ''
      };
    },
    mounted() {
        this.loadGoogleMaps();
    },
    methods: {
    loadGoogleMaps() {
      const googleMapsScript = document.createElement('script');
      console.log(process.env.VUE_APP_GOOGLE_MAPS_API_KEY)
      googleMapsScript.src = `https://maps.googleapis.com/maps/api/js?key=${process.env.VUE_APP_GOOGLE_MAPS_API_KEY}&libraries=places`;
      googleMapsScript.async = true;
      googleMapsScript.defer = true;
      googleMapsScript.onload = this.initializeAutocomplete;
      document.head.appendChild(googleMapsScript);
    },
    initializeAutocomplete() {
      const input = this.$refs.autocomplete.$el.querySelector('input');
      const autocomplete = new google.maps.places.Autocomplete(input);
      
      autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place.geometry) {
          this.center = {
            lat: place.geometry.location.lat(),
            lng: place.geometry.location.lng(),
          };
          this.address = place.formatted_address;
          this.city = this.getCityFromAddressComponents(place.address_components);
          this.goToPriorities()
        }
      });
    },

    getCityFromAddressComponents(addressComponents) {
      let city = null;

      // Loop through address components to find the locality (city)
      if (addressComponents) {
        addressComponents.forEach((component) => {
          if (component.types.includes('locality')) {
            city = component.long_name; // You can use 'short_name' if needed
          }
        });
      }

      return city;
    },
    
      // updateAddress() {
      //   const autocomplete = new google.maps.places.Autocomplete(
      //     this.$refs.autocomplete.$el.querySelector('input')
      //   );
  
      //   google.maps.event.addListener(autocomplete, 'place_changed', () => {
      //     const place = autocomplete.getPlace();
      //     if (place.geometry) {
      //       this.center = {
      //         lat: place.geometry.location.lat(),
      //         lng: place.geometry.location.lng(),
      //       };
      //       this.address = place.formatted_address;
      //     }
      //   });
      // },
      updateMapLocation(event) {
        this.center = {
          lat: event.latLng.lat(),
          lng: event.latLng.lng(),
        };
      },
      fetchAirQualityAndPollen() {
        const lat = this.center.lat;
        const lng = this.center.lng;
  
        this.fetchAirQuality(lat, lng);
        this.fetchPollenInfo(lat, lng);
      },
      async fetchAirQuality(lat, lng) {
        try {
          const response = await fetch(
            `https://maps.googleapis.com/maps/api/airquality?lat=${lat}&lng=${lng}&key=${process.env.VUE_APP_GOOGLE_MAPS_API_KEY}`
          );
          const data = await response.json();
          this.airQuality = data.result.measurements[0].value;
        } catch (error) {
          console.error('Error fetching air quality:', error);
        }
      },
      async fetchPollenInfo(lat, lng) {
        try {
          const response = await fetch(
            `https://maps.googleapis.com/maps/api/pollen?lat=${lat}&lng=${lng}&key=${process.env.VUE_APP_GOOGLE_MAPS_API_KEY}`
          );
          const data = await response.json();
          this.pollenInfo = data.result.pollen_level;
        } catch (error) {
          console.error('Error fetching pollen info:', error);
        }
      },
      goToPriorities() {
        this.$emit('locationSelected', {
          city: this.city,
          address: this.address,
          lat: this.center.lat,
          lng: this.center.lng,
        });
      },
    },
  };
  </script>
  
  <style scoped>
  .location-selection-container {
    padding: 40px;
    max-width: 100%;
  }
  
  .header-section {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .header-title {
    font-size: 3rem;
    color: #2c3e50;
    margin: 0;
  }
  
  .header-subtitle {
    font-size: 1.5rem;
    font-weight: 300;
    color: #34495e;
    margin: 5px 0;
  }
  
  .header-tagline {
    font-size: 1.2rem;
    font-weight: 300;
    color: #7f8c8d;
  }
  
  .section-title {
    font-size: 2rem;
    margin-bottom: 10px;
    color: #2c3e50;
    font-weight: 600;
  }
  
  .location-input {
    margin-bottom: 20px;
  }
  
  .map-container {
    border: 2px solid #bdc3c7;
    border-radius: 10px;
    overflow: hidden;
  }
  
  .check-btn {
    background-color: #3498db;
    color: white;
    font-weight: bold;
    margin-top: 20px;
  }
  
  .next-btn {
    background-color: #27ae60;
    color: white;
    font-weight: bold;
    margin-top: 20px;
  }
  
  .info-section {
    margin-top: 20px;
    font-size: 1.2rem;
    color: #2c3e50;
    text-align: center;
  }
  </style>
  