import Card from './components/cards/Card';
import BaseInput from './components/inputs/BaseInput';
import BaseRadio from './components/inputs/BaseRadio';
import BaseCheckbox from './components/inputs/BaseCheckbox';

import {library} from '@fortawesome/fontawesome-svg-core'
import {faChartLine, faDice, faUserCircle, faUsers} from '@fortawesome/free-solid-svg-icons'
import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome'


const GlobalComponents = {
    install(Vue) {
        library.add(faDice);
        library.add(faUsers);
        library.add(faUserCircle);
        library.add(faChartLine);
        Vue.component('font-awesome-icon', FontAwesomeIcon);
        Vue.component(Card.name, Card);
        Vue.component(BaseInput.name, BaseInput);
        Vue.component(BaseRadio.name, BaseRadio);
        Vue.component(BaseCheckbox.name, BaseCheckbox);
    }
};

export default GlobalComponents;
