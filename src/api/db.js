import axios from 'axios'

function getApiUrl(name) {
    return '/db/api/' + name
}

function postRequest(apiUrl, data) {
    return axios({
        method: 'post',
        url: apiUrl,
        headers: {
            'Content-Type': 'application/json'
        },
        data: data
    })
}

function wrapResult(flag, data) {
    return {
        flag: flag,
        data: data
    }
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
                    return wrapResult(false, '用户已存在')
                }
            }
            return wrapResult(false, '服务器错误')
        })
}

export async function login(userInfo) {
    return await postRequest(getApiUrl('login'), userInfo)
        .then((resp) => {
            return {
                flag: true,
                data: resp.data.info
            }
        })
        .catch((err) => {
            const resp = err.response
            if (resp.status == 404) {
                return wrapResult(false, '用户不存在')
            } else if (resp.status == 403) {
                return wrapResult(false, '密码错误')
            }
            return wrapResult(false, '服务器错误')
        })
}
