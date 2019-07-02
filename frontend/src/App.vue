<template>
  <v-app>
    <app-header></app-header>
    <v-content>
      <router-view></router-view>
    </v-content>
    <app-footer></app-footer>
  </v-app>
</template>

<script>
  import AppHeader from './apps/chat/AppHeader.vue'
  import AppChat from "./apps/chat/AppChat"
  import AppFooter from "./apps/chat/AppFooter"
  import AppSignIn from "./apps/chat/AppSignIn"
  import AppHome from "./apps/chat/AppHome"
  import AppSignUp from "./apps/chat/AppSignUp"

  export default {
    components: {AppSignIn, AppFooter, AppChat, AppHeader, AppHome, AppSignUp},
    created() {
      this.$store.dispatch('SET_USERNAME', window.APP_DATA.username)
      this.$store.dispatch('SET_IS_STAFF', window.APP_DATA.is_staff)
    }
  }

</script>

<style>

</style>
