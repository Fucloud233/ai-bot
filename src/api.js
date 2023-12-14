import axios from 'axios'

function getApiUrl(name) {
    return '/api/' + name
}

export async function chat(messages) {
    const apiUrl = getApiUrl('chat')

    return await axios({
        method: 'post',
        url: apiUrl,
        headers: {
            'Content-Type': 'application/json'
        },
        data: {
            messages: messages
        }
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
