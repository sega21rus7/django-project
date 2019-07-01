import Vuex from 'vuex'
import Vue from "vue"

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
      username: ''
    },
    getters: {
      USERNAME: state => state.username
    },
    mutations: {
      SET_USERNAME(state, payload) {
        state.username = payload
      }
    },
    actions: {
      SET_USERNAME(context, payload) {
        context.commit('SET_USERNAME', payload)
      }
    },
  }
)
