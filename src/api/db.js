import axios from 'axios'

function getApiUrl(name) {
    return '/db/api/' + name
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

export async function register(userInfo) {
    return await postRequest(getApiUrl('register'), userInfo)
        .then((resp) => {
            return {
                flag: true
            }
        })
        .catch((err) => {
            const resp = err.response

            if (resp.status == 400) {
                if (resp.data.code == 2002) {
                    return {
                        flag: false,
                        data: '用户已存在'
                    }
                }
            }

            return {
                flag: false,
                data: '服务器错误'
            }
        })
}
