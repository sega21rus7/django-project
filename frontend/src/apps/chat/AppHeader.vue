<template>
  <div>
    <v-navigation-drawer absolute class="hidden-md-and-up" temporary v-model="drawer">
      <v-list class="primary" dark>

        <v-list-tile :key="item.title"
                     :to="item.root" flat v-for="item in headerDynamicItems" v-model="item.model">
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

        <v-list-tile :href="item.root"
                     :key="item.title" flat v-for="item in headerStaticItems" v-model="item.model">
          <v-list-tile-action>
            <v-icon v-html="item.icon"></v-icon>
          </v-list-tile-action>
          <v-list-tile-content>
            <v-list-tile-title v-text="item.title"></v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>

      </v-list>
    </v-navigation-drawer>

    <v-toolbar class="primary" dark>
      <v-toolbar-side-icon @click.stop="drawer = !drawer" class="hidden-md-and-up"></v-toolbar-side-icon>
      <router-link style="cursor:pointer" tag="span" to="/">
        <v-toolbar-title class="text-uppercase orange--text">Test website</v-toolbar-title>
      </router-link>
      <v-spacer></v-spacer>
      <v-toolbar-items class="hidden-sm-and-down">

        <v-btn :key="item.title" :to="item.root" flat v-for="item in headerDynamicItems">
          <v-icon left v-html="item.icon"></v-icon>
          {{item.title}}
        </v-btn>

        <v-btn :href="item.root" :key="item.title" flat v-for="item in headerStaticItems">
          <v-icon left v-html="item.icon"></v-icon>
          {{item.title}}
        </v-btn>

      </v-toolbar-items>
    </v-toolbar>
  </div>

</template>

<script>
  export default {
    name: 'AppHeader',
    data() {
      return {
        drawer: false,
      }
    },
    computed: {
      get_username: function () {
        return this.$store.getters.USERNAME
      },
      is_login: function () {
        return this.get_username.length > 0
      },
      headerStaticItems() {
        if (this.is_login)
          return [
            {
              icon: 'verified_user',
              title: 'Admin panel',
              root: '/admin',
            },
            {
              icon: 'exit_to_app',
              title: 'Sign out',
              root: '/sign_out',
            },
          ]
      },
      headerDynamicItems() {
        if (this.is_login)
          return [
            {
              icon: 'chat',
              title: 'Chat',
              root: '/chat',
            },]
        return [
          {
            icon: 'lock_open',
            title: 'Sign up',
            root: '/sign_up',
          },
          {
            icon: 'input',
            title: 'Sign in',
            root: '/sign_in',
          },
        ]
      },
    }
  }
</script>
<style scoped>

</style>
