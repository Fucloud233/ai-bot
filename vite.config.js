import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { parseWidth } from 'element-plus/es/components/table/src/util'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    server: {
        port: 6060,
        proxy: {
            // '/db/api': {
            //     target: 'http://127.0.0.1:6062/',
            //     changeOrigin: true,
            //     rewrite: (path) => path.replace(/^\/db\/api/, '')
            // },
            '/api': {
                target: 'http://127.0.0.1:6062/',
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    }
})
