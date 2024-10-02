import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Make sure you import the router
import VueGoogleMaps from '@fawmi/vue-google-maps';
import vuetify from './plugins/vuetify'; // Import Vuetify setup if you're using it

createApp(App)
  .use(VueGoogleMaps, {
    load: {
      key: process.env.VUE_APP_GOOGLE_MAPS_API_KEY,
      libraries: 'places',
    },
  })
  .use(router)
  .use(vuetify)
  .mount('#app');
  