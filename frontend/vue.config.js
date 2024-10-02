const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',

  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',
        ws: true,
        changeOrigin: true
      },
      
    }
  },

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		}
  }
})
