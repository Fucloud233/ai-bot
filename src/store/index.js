import { createStore } from 'vuex'

const store = createStore({
    state() {
        return {
            hasLogged: false,
            userInfo: {
                phone: ''
            }
        }
    },
    mutations: {
        login(state, phone) {
            state.hasLogged = true
            state.userInfo.phone = phone
        }
    }
})

export default store
