export function getRoleLabel(roleName) {
    console.log(roleName)

    switch (roleName) {
        case 'parent':
            return '父母'
        case 'bestie':
            return '闺蜜'
        case 'friend':
            return '朋友'
        case 'doctor':
            return '心理医生'
        default:
            return ''
    }
}

export function getRoleProfileUrl(role) {
    return `/src/assets/profile/${role}.png`
}

export const delimiter = '\n\n'

export const USER = 'user'
export const ASSISTANT = 'assistant'

/* listener mechanism
 * encapsulate the interface to split and merge messages
 */
export function splitMessages(message) {
    return message.split(delimiter)
}
export function mergeMessages(messages) {
    return messages.join(delimiter)
}
