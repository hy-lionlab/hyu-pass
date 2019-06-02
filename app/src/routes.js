import Vue from 'vue';
import Router from 'vue-router';

import Intro from './pages/Intro';
import Request from './pages/Request';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'Intro',
      component: Intro,
    },
    {
      path: '/request',
      name: 'Request',
      component: Request,
    },
  ],
});
