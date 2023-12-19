import axios from 'axios'

export function postRequest(apiUrl, data) {
    return axios({
        method: 'post',
        url: apiUrl,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
}

export function putRequest(apiUrl, data) {
    return axios({
        method: 'put',
        url: apiUrl,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
}

export function getRequest(apiUrl) {
    return axios({
        method: 'get',
        url: apiUrl,
        headers: {
            'Content-Type': 'application/json'
        }
    })
}

export function getApiUrl(name, origin_params) {
    var apiUrl = '/api/' + name

    if (origin_params !== undefined) {
        var params = Object.entries(origin_params)

        if (params.length != 0) {
            apiUrl += '?'
            for (const param of params) {
                apiUrl += `${param[0]}=${param[1]}&`
            }
        }
        // kill the last &
        apiUrl = apiUrl.slice(0, -1)
    }

    return apiUrl
}

export function wrapResult(flag, data) {
    return {
        flag: flag,
        data: data
    }
}
