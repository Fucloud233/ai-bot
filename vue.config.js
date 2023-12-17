const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
    transpileDependencies: true,
    devServer: {
        port: 6060,
        proxy: {
            '/db/api': {
                target: 'http://127.0.0.1:6062/',
                changeOrigin: true,
                ws: false,
                pathRewrite: {
                    '^/db/api': ''
                }
            },
            '/api': {
                target: 'http://127.0.0.1:6061/',
                changeOrigin: true,
                ws: false,
                pathRewrite: {
                    '^/api': ''
                }
            }
        }
    }
})
