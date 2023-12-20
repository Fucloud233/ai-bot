import { createRouter, createWebHashHistory } from 'vue-router'
import store from '../store'

const routes = [
    {
        path: '/',
        name: 'login',
        component: () => import('../pages/LoginRegister.vue')
    },
    {
        path: '/talk/:role/',
        name: 'talk',
        component: () => import('../pages/TalkRoom.vue')
    },
    {
        path: '/main',
        name: 'main',
        component: () => import('../pages/RoleList.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
})

router.beforeEach(async (to, from) => {
    const hasLogged = store.state.hasLogged

    if (!hasLogged && to.name !== 'login') {
        return { name: 'login' }
    } else if (hasLogged && to.name == 'login') {
        return { name: 'main' }
    }
})

export default router
