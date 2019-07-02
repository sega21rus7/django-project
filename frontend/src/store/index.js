import Vuex from 'vuex'
import Vue from "vue"

Vue.use(Vuex);

export default new Vuex.Store({
    state: {
      username: '',
      is_staff: false,
    },
    getters: {
      USERNAME: state => state.username,
      IS_STAFF: state => state.is_staff
    },
    mutations: {
      SET_USERNAME(state, payload) {
        state.username = payload
      },
      SET_IS_STAFF(state, payload){
        state.is_staff = payload
      }
    },
    actions: {
      SET_USERNAME(context, payload) {
        context.commit('SET_USERNAME', payload)
      },
      SET_IS_STAFF(context, payload){
        context.commit('SET_IS_STAFF', payload)
      }
    },
  }
)
