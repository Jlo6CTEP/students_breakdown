import Vue from 'vue';
import VeeValidate from 'vee-validate';

import {store} from './_store';
// setup fake backend
import {configureFakeBackend, router} from './_helpers';
import App from './app/App';

Vue.use(VeeValidate);

configureFakeBackend();

new Vue({
    el: '#app',
    router,
    store,
    render: h => h(App)
});