// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import store from './store'
import Axios from 'axios'
import lodash from 'lodash'
import vuetify from '@/plugins/vuetify' // path to vuetify export

window._ = lodash
window.axios = Axios.create({
  baseURL: process.env.API_URL,
  timeout: 10000
});

if(localStorage.token){
  axios.defaults.headers.common['Authorization'] = 'Token '+ localStorage.token;
}

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  store,
  router,
  vuetify,
  components: { App },
  template: '<App/>'
})
