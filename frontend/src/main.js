import 'style/style'

import Vue from 'vue'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'

import App from './App.vue'
import AppChat from "./apps/chat/AppChat"
import AppSignIn from "./apps/chat/AppSignIn"
import AppSignUp from "./apps/chat/AppSignUp"
import AppHome from "./apps/chat/AppHome"
import axios from 'axios'
import store from './store'

Vue.use(VueRouter);
Vue.use(Vuetify);

// Make Axios play nice with Django CSRF
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

const router = new VueRouter({
  routes: [
    {path: '/chat', component: AppChat},
    {path: '/sign_in', component: AppSignIn},
    {path: '/sign_up', component: AppSignUp},
    {path: '/', component: AppHome},
  ],
});

new Vue({
  el: '#main',
  router: router,
  render: h => h(App),
  store: store
});
