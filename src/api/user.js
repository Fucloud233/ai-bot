import { getUserApiUrl, postRequest, wrapResult } from './utils'
import * as utils from './utils'

// register: it will complete 2 works
// 1. add user info into database, and init the role description (go-backend)
// 2. init vector database to store and query message (py-backend)
export async function register(userInfo) {
    postRequest(utils.getApiUrl('vectordb/init/all'), {
        phone: userInfo['phone']
    })

    return await postRequest(getUserApiUrl('register'), userInfo)
        .then(() => {
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
