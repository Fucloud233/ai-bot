import { getApiUrl, getRequest, postRequest, deleteRequest, wrapResult } from './utils'
import * as utils from './utils'

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
    // get botRole description
    const description = await getRequest(utils.getUserApiUrl('role/prompt'), {
        phone: phone,
        botRole: botRole
    })
        .then((resp) => {
            return resp.data['rolePrompt']
        })
        .catch(() => {
            return ''
        })

    return await postRequest(getApiUrl('chat/enhance'), {
        phone: phone,
        botRole: botRole,
        botRoleDescription: description,
        userMessage: message
    })
        .then((resp) => {
            return wrapResult(true, resp.data.message)
        })
        .catch(() => {
            return wrapResult(false, '')
        })
}

export async function deleteAllMessage(phone, botRole) {
    return await deleteRequest(getApiUrl('vectordb/messages/all'), {
        phone: phone,
        botRole: botRole
    })
        .then(() => {})
        .catch(() => {})
}

export async function getNewestMessages(phone, botRole, number, offset) {
    return await getRequest(getApiUrl('vectordb/messages/nearest'), {
        phone: phone,
        botRole: botRole,
        number: number,
        offset: offset,
        // set -1 to ignore time limitation
        n: -1
    })
        .then((resp) => {
            return { data: resp.data['messages'] }
        })
        .catch((err) => {
            return { data: [] }
        })
}
