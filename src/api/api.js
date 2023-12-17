import axios from 'axios'

function getApiUrl(name) {
    return '/api/' + name
}

async function postRequest(apiUrl, data) {
    return await axios({
        method: 'post',
        url: apiUrl,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
        .then((resp) => {
            return {
                data: resp.data,
                flag: true
            }
        })
        .catch((err) => {
            return {
                data: err.response.data,
                flag: false
            }
        })
}

export async function chat(messages) {
    const apiUrl = getApiUrl('chat')

    return await postRequest(apiUrl, {
        messages: messages
    })
}

export async function chatWithRole(messages, role) {
    const apiUrl = getApiUrl('chat') + '/' + role

    return await postRequest(apiUrl, {
        messages: messages,
        role: role
    })
}
