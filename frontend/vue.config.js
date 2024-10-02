const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  outputDir: 'dist',

  // Set publicPath depending on the environment
  publicPath: process.env.NODE_ENV === 'production' ? '/static/' : '/',

  // Configure the devServer for local development
  devServer: {
    port: 8080,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000/',  // Django backend
        ws: true,
        changeOrigin: true
      },
    }
  },

  pluginOptions: {
    vuetify: {
      // Vuetify configuration
      // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
    }
  }
});