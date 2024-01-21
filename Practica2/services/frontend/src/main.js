import BootstrapVue from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import matches from './components/Matches.vue'
import login from './components/Login.vue'
import VueSimpleAlert from 'vue-simple-alert'

Vue.component('matches', matches)
Vue.component('login', login)

Vue.use(VueSimpleAlert)
Vue.use(BootstrapVue)
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: {
    App: App,
    matches: matches,
    login: login
  },
  template: '<App/>'
})
