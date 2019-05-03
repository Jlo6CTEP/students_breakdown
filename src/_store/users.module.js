import {userService} from '../_services';

const state = {
    users: {items: JSON.parse(localStorage.getItem('users'))},
};

const actions = {
    getAll({commit}) {
        commit('getAllRequest');

        userService.getAll()
            .then(
                users => commit('getAllSuccess', users),
                error => commit('getAllFailure', error)
            );
    },
    getById({dispatch, commit}, id) {
        commit('getByIdRequest');

        userService.getById(id)
            .then(
                user => {
                    commit('getByIdSuccess', user);
                },
                error => {
                    commit('getByIdFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    update({dispatch, commit}, user) {
        let id = user.id;
        commit('updateRequest', id);

        userService.update(user)
            .then(
                user => {
                    commit('updateSuccess', user);
                },
                error => {
                    commit('updateFailure', {error, id});
                    dispatch('alert/error', error, {root: true});
                }
            )
    },

    delete({commit}, id) {
        commit('deleteRequest', id);

        userService.delete(id)
            .then(
                user => commit('deleteSuccess', id),
                error => commit('deleteSuccess', {id, error: error.toString()})
            );
    }
};

const mutations = {
    getAllRequest(state) {
        state.users = {loading: true};
    },
    getAllSuccess(state, users) {
        state.users = {items: users};
    },
    getAllFailure(state, error) {
        state.users = {error};
    },
    getByIdRequest(state, id) {
    },
    getByIdSuccess(state, user) {
    },
    getByIdFailure(state, {error, id}) {
    },
    updateRequest(state, id) {
        console.log("REQUEST");
        state.users.items = state.users.items.map(user =>
            user.id === id
                ? {...user, updating: true}
                : user
        );
    },
    updateSuccess(state, user) {
        state.users.items = state.users.items.map(u =>
            u.id === user.id
                ? user
                : u);
    },
    updateFailure(state, {error, id}) {
        state.users.items = state.users.items.map(users => {
            if (users.id === id) {
                const {updating, ...userCopy} = users;
                return {...userCopy, updateError: error};
            }
            return users;
        });
    },

    deleteRequest(state, id) {
        // add 'deleting:true' property to user being deleted
        state.all.items = state.all.items.map(user =>
            user.id === id
                ? {...user, deleting: true}
                : user
        )
    },
    deleteSuccess(state, id) {
        // remove deleted user from state
        state.all.items = state.all.items.filter(user => user.id !== id)
    },
    deleteFailure(state, {id, error}) {
        // remove 'deleting:true' property and add 'deleteError:[error]' property to user
        state.all.items = state.all.items.map(user => {
            if (user.id === id) {
                // make copy of user without 'deleting:true' property
                const {deleting, ...userCopy} = user;
                // return copy of user with 'deleteError:[error]' property
                return {...userCopy, deleteError: error};
            }

            return user;
        })
    }
};

export const users = {
    namespaced: true,
    state,
    actions,
    mutations
};
