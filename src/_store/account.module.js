import {userService} from '../_services';
import {store} from './index';
import {router} from '../router';

const user = JSON.parse(localStorage.getItem('user'));
const state = user
    ? {auth: {loggedIn: true}, user}
    : {auth: {}, user: null};

const getters = {
    getStatus: state => state.user ? state.user.status : 'not-auth',
    getUrl: state => url => {
        let status = state.user ? state.user.status : 'not-auth';
        return `/` + status + url;
    }
};

const actions = {
    login({dispatch, commit}, {username, password}) {
        commit('loginRequest', {username});

        userService.login(username, password)
            .then(
                user => {
                    commit('loginSuccess', user);
                    router.push(store.getters["account/getUrl"](''));
                },
                error => {
                    commit('loginFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            );
    },
    logout({commit}) {
        userService.logout();
        commit('logout');
    },
    register({dispatch, commit}, user) {
        commit('registerRequest', user);

        userService.register(user)
            .then(
                user => {
                    commit('registerSuccess', user);
                    router.push('/login');
                    setTimeout(() => {
                        // display success message after route change completes
                        dispatch('alert/success', 'Registration successful', {root: true});
                    })
                },
                error => {
                    commit('registerFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            );
    }
};

const mutations = {
    loginRequest(state, user) {
        state.auth = {loggingIn: true};
        state.user = user;
    },
    loginSuccess(state, user) {
        state.auth = {loggedIn: true};
        state.user = user;
    },
    loginFailure(state) {
        state.auth = {};
        state.user = null;
    },
    logout(state) {
        state.auth = {};
        state.user = null;
    },
    registerRequest(state, user) {
        state.auth = {registering: true};
    },
    registerSuccess(state, user) {
        state.auth = {};
    },
    registerFailure(state, error) {
        state.auth = {};
    }
};

export const account = {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
