import { createRouter, createWebHistory } from 'vue-router';
import LandingPage from '@/components/LandingPage.vue';
// import LocationDetails from '@/components/LocationSelection.vue';
// import PrioritySelection from '@/components/PrioritySelection.vue';
// import SelectionAndResults from '@/components/SelectionAndResults.vue';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
//   {
//     path: '/location-details',
//     name: 'LocationDetails',
//     component: LocationDetails,
//     props: true,
//   },
//   {
//     path: '/priority-selection',
//     name: 'PrioritySelection',
//     component: PrioritySelection,
//     props: true,
//   },
//   {
//     path: '/selection-results/:city',
//     name: 'SelectionAndResults',
//     component: SelectionAndResults,
//     props: true
//   }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
