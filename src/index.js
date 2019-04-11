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

Vue.component('expander', {
    template: '<div class="Expander">\n' +
        '    <div class="Expander__trigger" \n' +
        '      @click="open=!open" \n' +
        '      :class="open?\'active\':\'beforeBorder\'">\n' +
        '        <svg \n' +
        '          class="Expander__trigger-Icon" \n' +
        '          :class="{open:open}" \n' +
        '          width="40" height="12" \n' +
        '          stroke="cornflowerblue">\n' +
        '            <polyline points="12,2 20,10 28,2" stroke-width="3" fill="none"></polyline>\n' +
        '        </svg>\n' +
        '        {{ title }}\n' +
        '    </div>\n' +
        '    <transition :name="animation">\n' +
        '        <div class="Expander__body" v-show="open">\n' +
        '            <slot></slot>\n' +
        '        </div>\n' +
        '    </transition>\n' +
        '</div>',
    props: {
        title: {
            type: String,
            default:
                'title'
        }
        ,
        animation: {
            type: String,
            default:
                'rightToLeft'
            // validator: prop => ['leftToRight', 'bounceIn', 'bottomToTop'].includes(prop)
        }
    }
    ,
    data() {
        return {
            open: false
        }
    }
});