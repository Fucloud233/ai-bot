import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
    {
        path: '/',
        redirect: '/talk'
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('../components/LoginRegister.vue')
    },
    {
        path: '/talk',
        name: 'talk',
        component: () => import('../components/TalkRoom.vue')
    }
]

const router = createRouter({
    history: createWebHashHistory(),
    routes: routes
})

export default router
