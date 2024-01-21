import Vue from 'vue'
import Router from 'vue-router'
import Matches from '../components/Matches'
import process from 'shelljs'
import Login from '../components/Login.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'matches',
      component: Matches
    },
    {
      path: '/userlogin',
      name: 'login',
      component: Login
    }
  ]
})
