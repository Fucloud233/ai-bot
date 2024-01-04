import { getUserApiUrl, postRequest, wrapResult } from './utils'

export async function register(userInfo) {
    return await postRequest(getUserApiUrl('register'), userInfo)
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
    return await postRequest(getUserApiUrl('login'), userInfo)
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
