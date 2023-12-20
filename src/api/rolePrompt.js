import { getRequest, getApiUrl, putRequest } from './utils'

export async function getRolePrompt(phone, botRole) {
    return await getRequest(getApiUrl('role/prompt'), {
        phone: phone,
        botRole: botRole
    })
        .then((resp) => {
            const rolePrompt = resp.data.rolePrompt
            if (rolePrompt === undefined) {
                return ''
            }

            return resp.data.rolePrompt
        })
        .catch(() => {
            return ''
        })
}

export async function postRolePrompt(phone, botRole, rolePrompt) {
    const apiUrl = getApiUrl('role/prompt')

    return await putRequest(apiUrl, {
        phone: phone,
        botRole: botRole,
        rolePrompt: rolePrompt
    })
        .then(() => {
            return {
                flag: true
            }
        })
        .catch((error) => {
            return {
                flag: true,
                data: error.response.data
            }
        })
}
