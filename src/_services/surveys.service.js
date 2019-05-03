import {authHeader} from '../_helpers';

const apiUrl = 'http://127.0.0.1:8000';

export const surveyService = {
    getAllCourses,
    getCoursesByUserId,
    getGroupsByCourseId: getGroupsByCourse,
    create,
    getAll,
    getById,
    update,
    delete: _delete
};

function getAllCourses() {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/course`, requestOptions).then(handleResponse);
}

function getCoursesByUserId(user_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/course/${user_id}`, requestOptions).then(handleResponse);
}

function getGroupsByCourse(course_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/groups/${course_id}`, requestOptions).then(handleResponse);
}

function create(user_id, survey_name, group_by, description, additional_info, groups, topics) {
    const requestOptions = {
        method: 'POST',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
        body: JSON.stringify({user_id, survey_name, group_by, description, additional_info, groups, topics})
    };

    return fetch(`${apiUrl}/surveys/create`, requestOptions).then(handleResponse);
}

function getAll(user_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/${user_id}`, requestOptions).then(handleResponse);
}

function getById(user_id, survey_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/${user_id}/${survey_id}`, requestOptions).then(handleResponse);
}

function update(user_id, survey) {
    const requestOptions = {
        method: 'PUT',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
        body: JSON.stringify(survey)
    };

    return fetch(`${apiUrl}/surveys/${user_id}/${survey.id}`, requestOptions).then(handleResponse);
}

function _delete(user_id, survey_id) {
    const requestOptions = {
        method: 'DELETE',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/${user_id}/${survey_id}`, requestOptions).then(handleResponse);
}

function handleResponse(response) {
    return response.text().then(text => {
        const data = text && JSON.parse(text);
        if (!response.ok) {
            if (response.status === 401) {
                // auto logout if 401 response returned from api
                logout();
                location.reload(true);
            }

            const error = (data && data.message) || response.statusText;
            return Promise.reject(error);
        }

        return data;
    });
}
