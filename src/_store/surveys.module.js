import {surveyService} from '../_services';

const state = {
    courses: {},
    groups: {},
    surveys: {},
    survey: null
};

const getters = {
    loading: state => {
        return state.courses.loading || state.groups.loading || state.surveys.loading;
    },
    error: state => {
        return state.courses.error || state.groups.error || state.surveys.error;
    }
};

const actions = {
    getAllCourses({dispatch, commit}) {
        commit('getAllCoursesRequest');

        surveyService.getAllCourses()
            .then(
                courses => {
                    commit('getAllCoursesSuccess', courses);
                },
                error => {
                    commit('getAllCoursesFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    getGroupsByCourseId({dispatch, commit}, {course_id}) {
        commit('getGroupsByCourseIdRequest');

        surveyService.getGroupsByCourseId(course_id)
            .then(
                groups => {
                    commit('getGroupsByCourseIdSuccess', groups);
                },
                error => {
                    commit('getGroupsByCourseIdFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    create({dispatch, commit}, {user_id, survey_name, group_by, description, additional_info, groups, topics}) {
        commit('createRequest', {user_id, survey_name});

        surveyService.create(user_id, survey_name, group_by, description, additional_info, groups, topics)
            .then(
                survey => {
                    commit('createSuccess', survey);
                },
                error => {
                    commit('createFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            );
    },
    getAll({commit}, {user_id}) {
        commit('getAllRequest');

        surveyService.getAll(user_id)
            .then(
                users => commit('getAllSuccess', users),
                error => commit('getAllFailure', error)
            );
    },
    getById({dispatch, commit}, {user_id, survey_id}) {
        commit('getByIdRequest');

        surveyService.getById(user_id, survey_id)
            .then(
                survey => {
                    commit('getByIdSuccess', survey);
                },
                error => {
                    commit('getByIdFailure', error);
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    update({dispatch, commit}, {user_id, survey}) {
        let survey_id = survey.id;
        commit('updateRequest', survey_id);

        surveyService.update(user_id, survey)
            .then(
                survey => {
                    commit('updateSuccess', survey);
                },
                error => {
                    commit('updateFailure', {error, survey_id});
                    dispatch('alert/error', error, {root: true});
                }
            )
    },
    delete({commit}, {user_id, survey_id}) {
        commit('deleteRequest', survey_id);

        surveyService.delete(user_id, survey_id)
            .then(
                user => commit('deleteSuccess', survey_id),
                error => commit('deleteFailure', {survey_id, error: error.toString()})
            );
    }
};

const mutations = {
    getAllCoursesRequest(state) {
        state.courses = {loading: true};
    },
    getAllCoursesSuccess(state, courses) {
        state.courses = {loading: false, items: courses};
    },
    getAllCoursesFailure(state, error) {
        state.courses = {error};
    },
    getGroupsByCourseIdRequest(state) {
        state.groups = {loading: true};
    },
    getGroupsByCourseIdSuccess(state, groups) {
        state.groups = {loading: false, items: groups};
    },
    getGroupsByCourseIdFailure(state, error) {
        state.groups = {error};
    },
    createRequest(state) {
        state.survey = {};
    },
    createSuccess(state, survey) {
        state.survey = survey;
    },
    createFailure(state, error) {
        state.survey = {error};
    },
    getAllRequest(state) {
        state.surveys = {loading: true};
    },
    getAllSuccess(state, surveys) {
        state.surveys = {loading: false, items: surveys};
    },
    getAllFailure(state, error) {
        state.surveys = {error};
    },
    getByIdRequest(state) {
        state.survey = {};
    },
    getByIdSuccess(state, survey) {
        state.survey = survey;
    },
    getByIdFailure(state) {
        state.survey = {};
    },
    updateRequest(state, id) {
        state.surveys.items = state.surveys.items.map(survey =>
            survey.id === id
                ? {...survey, updating: true}
                : survey
        );
        state.survey = {};
    },
    updateSuccess(state, survey) {
        state.surveys.items = state.surveys.items.map(s =>
            s.id === survey.id
                ? survey
                : s);
        state.survey = survey;
    },
    updateFailure(state, {error, survey_id: id}) {
        state.surveys.items = state.surveys.items.map(survey => {
            if (survey.id === id) {
                const {updating, ...surveyCopy} = survey;
                return {...surveyCopy, updateError: error};
            }
            return survey;
        });
        state.survey = null;
    },
    deleteRequest(state, id) {
        state.surveys.items = state.surveys.items.map(survey =>
            survey.id === id
                ? {...survey, deleting: true}
                : survey
        )
    },
    deleteSuccess(state, id) {
        state.surveys.items = state.surveys.items.filter(survey => survey.id !== id);
        state.survey = null;
    },
    deleteFailure(state, {id, error}) {
        state.surveys.items = state.surveys.items.map(survey => {
            if (survey.id === id) {
                const {deleting, ...surveyCopy} = survey;
                return {...surveyCopy, deleteError: error};
            }

            return survey;
        });
        state.survey = null;
    }
};

export const surveys = {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
};
