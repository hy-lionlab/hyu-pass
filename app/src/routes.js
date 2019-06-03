import Vue from 'vue';
import Router from 'vue-router';

import Layouts from './pages/Layouts';
import Intro from './pages/Intro';
import Request from './pages/Request';

import Admin from './pages/admin/Index';
import AdminRequest from './pages/admin/Request';
import AdminKeyword from './pages/admin/Keyword';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Layouts,
      children: [
        {
          path: '',
          component: Intro,
        },
        {
          path: 'request',
          component: Request,
        },
      ],
    },
    {
      path: '/admin',
      component: Admin,
      children: [
        {
          path: 'requests',
          component: AdminRequest,
        },
        {
          path: 'keywords',
          component: AdminKeyword,
        },
      ],
    },
  ],
});
