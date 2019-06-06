import Vue from 'vue';
import Router from 'vue-router';

import Sorry from './pages/Sorry';

import Layouts from './pages/Layouts';
import Support from './pages/Support';
import Keyword from './pages/Keyword';
import Request from './pages/Request';

import Admin from './pages/admin/Index';
import AdminRequest from './pages/admin/Request';
import AdminKeyword from './pages/admin/Keyword';
import AdminSupport from './pages/admin/Support';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Layouts,
      children: [
        // ROOT PATH DEFAULT
        {
          path: '',
          redirect: 'requests',
        },
        {
          path: 'supports',
          component: Support,
        },
        {
          path: 'keywords',
          component: Keyword,
        },
        {
          path: 'requests',
          component: Request,
        },
      ],
    },
    {
      path: '/sorry',
      component: Sorry,
    },
    {
      path: '/admin',
      component: Admin,
      children: [
        {
          path: '',
          redirect: 'requests',
        },
        {
          path: 'requests',
          component: AdminRequest,
        },
        {
          path: 'keywords',
          component: AdminKeyword,
        },
        {
          path: 'supports',
          component: AdminSupport,
        },
      ],
    },
  ],
});
