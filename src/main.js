// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import {SBD} from './student-breakdown-dashboard';
import {router} from './router'
import {store} from './_store'
// setup fake backend
// import {configureFakeBackend} from './_helpers';

configureFakeBackend();


if (process.env.NODE_ENV !== 'production') {
    console.log('Looks like we are in development mode!');

}

Vue.use(SBD);
Vue.config.productionTip = false;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {App},
  template: '<App/>'
});
