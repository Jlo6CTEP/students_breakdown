import {teamService} from '../_services';

const state = {
    teams: {},
    team: null
};

const getters = {
    loading: state => {
        return state.teams.loading;
    },
    error: state => {
        return state.teams.error;
    }
};

const actions = {
    form({dispatch, commit}, {user_id, survey_id}) {
        commit('formRequest', {user_id, survey_id});

        teamService.form(user_id, survey_id)
            .then(
                team => {
                    commit('formSuccess', team);
                },
                error => {
                    commit('formFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            );
    },
    getAll({commit}, {user_id, survey_id}) {
        commit('getAllRequest');

        teamService.getAll(user_id, survey_id)
            .then(
                teams => commit('getAllSuccess', teams),
                error => commit('getAllFailure', error)
            );
    },
    getById({dispatch, commit}, {user_id, survey_id, team_id}) {
        commit('getByIdRequest');

        teamService.getById(user_id, survey_id, team_id)
            .then(
                team => {
                    commit('getByIdSuccess', team);
                },
                error => {
                    commit('getByIdFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    update({dispatch, commit}, {user_id, survey_id, team}) {
        let team_id = team.id;
        commit('updateRequest', team_id);

        teamService.update(user_id, survey_id, team)
            .then(
                survey => {
                    commit('updateSuccess', team);
                },
                error => {
                    commit('updateFailure', {error, team_id});
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    delete({commit}, {user_id, survey_id, team_id}) {
        commit('deleteRequest', team_id);

        teamService.delete(user_id, survey_id, team_id)
            .then(
                team => commit('deleteSuccess', team_id),
                error => commit('deleteFailure', {team_id, error: error.toString()})
            );
    }
};

const mutations = {
    formRequest(state) {
        state.teams = {forming: true};
    },
    createSuccess(state, teams) {
        state.teams = {items: teams};
    },
    createFailure(state, error) {
        state.teams = {error};
    },
    getAllRequest(state) {
        state.teams = {loading: true};
    },
    getAllSuccess(state, teams) {
        state.teams = {loading: false, items: teams};
    },
    getAllFailure(state, error) {
        state.teams = {error};
    },
    getByIdRequest(state) {
        state.team = {};
    },
    getByIdSuccess(state, team) {
        state.team = team;
    },
    getByIdFailure(state) {
        state.team = {};
    },
    updateRequest(state, id) {
        state.teams.items = state.teams.items.map(team =>
            team.id === id
                ? {...team, updating: true}
                : team
        );
        state.team = {};
    },
    updateSuccess(state, team) {
        state.teams.items = state.teams.items.map(t =>
            t.id === team.id
                ? team
                : t);
        state.team = team;
    },
    updateFailure(state, {error, team_id: id}) {
        state.teams.items = state.teams.items.map(team => {
            if (team.id === id) {
                const {updating, ...teamCopy} = team;
                return {...teamCopy, updateError: error};
            }
            return team;
        });
        state.team = {};
    },
    deleteRequest(state, id) {
        state.teams.items = state.teams.items.map(team =>
            team.id === id
                ? {...team, deleting: true}
                : team
        )
    },
    deleteSuccess(state, id) {
        state.teams.items = state.teams.items.filter(team => team.id !== id);
        state.team = null;
    },
    deleteFailure(state, {id, error}) {
        state.teams.items = state.teams.items.map(team => {
            if (team.id === id) {
                const {deleting, ...teamCopy} = team;
                return {...teamCopy, deleteError: error};
            }

            return team;
        });
        state.team = null;
    }
};

export const teams = {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};

