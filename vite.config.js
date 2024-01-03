import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 6060,
        proxy: {
            // python backend
            '/api': {
                target: 'http://127.0.0.1:6061/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            },
            // golang backend
            '/user/api': {
                target: 'http://127.0.0.1:6062/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/user\/api/, '')
            }
        }
    }
})
