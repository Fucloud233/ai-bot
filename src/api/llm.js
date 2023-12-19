import { getApiUrl, postRequest, wrapResult } from './utils'

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

export async function sendMessage(phone, botRole, message) {
    const apiUrl = getApiUrl('message')

    return await postRequest(apiUrl, {
        phone: phone,
        botRole: botRole,
        message: message
    })
        .then((resp) => {
            return wrapResult(true, resp.data.message)
        })
        .catch(() => {
            return wrapResult(false, '')
        })
}
