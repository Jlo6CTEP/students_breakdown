// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import {router} from './router'
import VueHead from 'vue-head'
import {store} from './_store'
import VeeValidate from 'vee-validate';
import VModal from 'vue-js-modal'
// setup fake backend
// import {configureFakeBackend} from './_helpers';

if (process.env.NODE_ENV !== 'production') {

    console.log('Looks like we are in development mode!');
}

Vue.use(VModal, {dynamic: true});
Vue.use(VueHead);
Vue.use(VeeValidate);
Vue.config.productionTip = false;

//configureFakeBackend();

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
