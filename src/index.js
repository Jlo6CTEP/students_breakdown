import Vue from 'vue';
import VeeValidate from 'vee-validate';
import VShowSlide from 'v-show-slide';

import {store} from './_store';
// setup fake backend
import {configureFakeBackend, router} from './_helpers';
import App from './app/App';

Vue.use(VeeValidate);
Vue.use(VShowSlide);

configureFakeBackend();

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});