// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import {router} from './router'
import VueHead from 'vue-head'
import {store} from './_store'
import VeeValidate from 'vee-validate';
// setup fake backend
import {configureFakeBackend} from './_helpers';

Vue.use(VueHead);
Vue.use(VeeValidate);
Vue.config.productionTip = false;

configureFakeBackend();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
})
