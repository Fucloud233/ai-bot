import axios from 'axios'

function getApiUrl(name) {
    return '/db/api/' + name
}

export async function getNewestMessages(phone, size) {
    return await axios({
        method: 'get',
        url: getApiUrl('messages'),
        params: {
            phone: phone,
            num: 5,
            size: size
        },
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then((resp) => {
            return {
                data: resp.data['messages']
            }
        })
        .catch(() => {
            return {}
        })
}
