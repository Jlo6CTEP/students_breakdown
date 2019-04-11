
export const getProject = function () {
    return fetch('http://localhost:8080/create_survey', {method: 'GET'});
};

export const saveProject = function (data) {
    return fetch('http://localhost:8080/create_survey', {method: 'POST', body:  JSON.stringify(data)});
};


