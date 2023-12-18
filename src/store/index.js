import { createStore } from 'vuex'

const store = createStore({
    state() {
        return {
            hasLogged: false
        }
    },
    mutations: {
        login(state) {
            state.hasLogged = true
        }
    }
})

export default store
