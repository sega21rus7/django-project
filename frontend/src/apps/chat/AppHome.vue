<template>
  <div>

    <v-layout row>
      <v-flex xs7>

      </v-flex>
      <v-flex xs5>
        <template>
          <div v-if="is_login">
            <v-alert :value="true" type="success">
              You are successfully signed in as <span class="username_style">{{ get_username }}</span>
            </v-alert>
          </div>
          <div v-else>
            <v-alert :value="true" type="error">
              You are unfortunately haven't signed in.
            </v-alert>
          </div>
        </template>
      </v-flex>
    </v-layout>


  </div>
</template>

<script>
  export default {
    name: "AppHome",
    computed: {
      get_username: function () {
        return this.$store.getters.USERNAME
      },
      is_login: function () {
        return this.get_username.length > 0
      }
    },
  }
</script>

<style scoped>
  .username_style {
    color: orange;
    text-decoration: underline;
    font-weight: bold;
  }

</style>
