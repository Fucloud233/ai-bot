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
