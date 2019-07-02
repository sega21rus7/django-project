<template>
  <v-container fill-height fluid>
    <v-layout align-center justify-center>
      <v-flex md4 sm8 xs12>
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark>
            <v-toolbar-title>Sign in form</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form v-model="valid" @keyup.enter.native="signIn">
              <v-text-field
                :rules="[rules.required].concat(rules.username)" clearable label="Login"
                name="login" prepend-icon="person" required type="text" v-model="username">
              </v-text-field>
              <v-text-field :append-icon="showPassword ? 'visibility' : 'visibility_off'"
                            :rules="[rules.required].concat(rules.password)"
                            :type="showPassword ? 'text' : 'password'"
                            @click:append="showPassword = !showPassword" clearable id="password" label="Password"
                            name="password"
                            prepend-icon="lock" required v-model="password">
              </v-text-field>
              <v-alert :value="true"
                         type="error"
                         v-if="errors"
                >
                  <p>We found out these errors in the form. Please correct it before continue.</p>
                  <div v-if="errors.username"><span class="fieldName">UserName</span> - {{errors.username}}</div>
                  <div v-if="errors.password"><span class="fieldName">Password</span> - {{errors.password}}</div>
                  <div v-if="errors.non_field_errors">{{errors.non_field_errors}}</div>
                </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="signIn" color="primary" flat v-bind:disabled="!valid">Sign in</v-btn>
          </v-card-actions>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "AppSignIn",
    data() {
      return {
        valid: false,
        username: '',
        password: '',
        response: '',
        showPassword: false,
        showConfirmPassword: false,
        rules: {
          required: value => !!value || 'This field must be required.',
          username: v => {
            return v.length >= 5 || 'Login must be more than 5 characters or equal to 5'
          },
          password: [
            v => v.length >= 6 || 'Password must be more than 6 characters or equal to 6',
            v => v.length <= 32 || 'Password must be less than 32 characters or equal to 32',
          ],
        },
        errors: null,
      }
    },
    methods: {
      signIn: function () {
        axios.post('./api/user/login/', {
          username: this.username,
          password: this.password,
        })
          .then(response => {
            console.log(response.data);
            // this.$router.push('/');
            document.location.href = '/';
          })
          .catch(error => {
              console.log(error);
              this.errors = error.response.data;
            }
          );
      },
    }
  }
</script>

<style scoped>
  .fieldName {
    text-decoration: underline;
    font-weight: bold;
  }
</style>
