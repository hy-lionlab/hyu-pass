import 'ant-design-vue/dist/antd.css';

import Vue from 'vue';
import VueProgressBar from 'vue-progressbar';
import Antd from 'ant-design-vue';

import App from './App';
import router from './routes';

/* Vue Configs */
Vue.config.productionTip = false;

/* Vue Libraries */
Vue.use(Antd);
Vue.use(VueProgressBar, {
  color: 'rgb(143, 255, 199)',
  failedColor: 'red',
  height: '2px',
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>',
});
