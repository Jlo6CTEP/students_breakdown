import {authHeader} from '../_helpers';

const apiUrl = 'http://127.0.0.1:8000';

export const teamService = {
    form,
    getAll,
    getById,
    update,
    delete: _delete
};

function form(user_id, survey_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/teams/form/${user_id}/${survey_id}`, requestOptions).then(handleResponse);
}

function getAll(user_id, survey_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/teams/${user_id}/${survey_id}`, requestOptions).then(handleResponse);
}

function getById(user_id, survey_id, team_id) {
    const requestOptions = {
        method: 'GET',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/${user_id}/${survey_id}/${team_id}`, requestOptions).then(handleResponse);
}

function update(user_id, survey_id, team) {
    const requestOptions = {
        method: 'PUT',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
        body: JSON.stringify(team)
    };

    return fetch(`${apiUrl}/surveys/${user_id}/${survey_id}/${team.id}`, requestOptions).then(handleResponse);
}

function _delete(user_id, survey_id, team_id) {
    const requestOptions = {
        method: 'DELETE',
        headers: {...authHeader(), 'Content-Type': 'application/json'},
    };

    return fetch(`${apiUrl}/surveys/${user_id}/${survey_id}/${team_id}`, requestOptions).then(handleResponse);
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
