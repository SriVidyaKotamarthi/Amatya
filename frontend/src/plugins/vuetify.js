// Styles
import '@mdi/font/css/materialdesignicons.css'; // Icon fonts
import 'vuetify/styles'; // Vuetify styles

// Vuetify
import { createVuetify } from 'vuetify';
import { VApp, VAppBar, VCard, VContainer, VRow, VCol } from 'vuetify/components';

// Create a Vuetify instance
const vuetify = createVuetify({
  components: {
    VApp,
    VAppBar,
    VCard,
    VContainer,
    VRow,
    VCol
  },
});

export default vuetify;
