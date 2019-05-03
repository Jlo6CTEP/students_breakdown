import VToolTip from 'v-tooltip';
import VueHead from 'vue-head'
import VeeValidate from 'vee-validate';
import VModal from 'vue-js-modal'
import Notification from './components/notifications/Notification';
import GlobalComponents from './globalComponents';
import 'bootstrap/dist/css/bootstrap.css';


export const SBD = {
    install(Vue) {
        Vue.use(GlobalComponents);
        Vue.use(VModal, {dynamic: true});
        Vue.use(VueHead);
        Vue.use(VeeValidate);
        Vue.use(Notification);
        Vue.use(VToolTip);
    }
};
