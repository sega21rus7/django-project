<template>
  <div>

    <v-container fill-height fluid>
      <v-layout align-center justify-center>
        <v-flex md4 sm8 xs12>
          <v-card class="elevation-12">
            <v-toolbar color="primary" dark>
              <v-toolbar-title>Sign up form</v-toolbar-title>
            </v-toolbar>
            <v-card-text>
              <v-form v-model="valid" @keyup.enter.native="signUp">
                <v-text-field
                  :rules="[rules.required].concat(rules.username)" clearable label="Login"
                  name="login" prepend-icon="person" required type="text" v-model="username">
                </v-text-field>
                <v-text-field :rules="[rules.required]" clearable label="Email" name="email"
                              prepend-icon="email" required type="text" v-model="email">
                </v-text-field>
                <v-text-field :append-icon="showPassword ? 'visibility' : 'visibility_off'"
                              :rules="[rules.required].concat(rules.password)"
                              :type="showPassword ? 'text' : 'password'" @click:append="showPassword = !showPassword"
                              clearable id="password" label="Password" name="password"
                              prepend-icon="lock" required
                              v-model="password">
                </v-text-field>
                <v-text-field :append-icon="showConfirmPassword ? 'visibility' : 'visibility_off'"
                              :rules="[rules.required].concat(rules.password)"
                              :type="showConfirmPassword ? 'text' : 'password'"
                              @click:append="showConfirmPassword = !showConfirmPassword"
                              clearable id="confirm_password" label="Confirm password" name="password"
                              prepend-icon="lock" required
                              v-model="confirm_password">
                </v-text-field>
                <v-alert :value="true"
                         type="error"
                         v-if="errors"
                >
                  <p>We found out these errors in the form. Please correct it before continue.</p>
                  <div v-if="errors.username"><span class="fieldName">Username</span> - {{errors.username}}</div>
                  <div v-if="errors.email"><span class="fieldName">Email</span> - {{errors.email}}</div>
                  <div v-if="errors.password"><span class="fieldName">Password</span> - {{errors.password}}</div>
                  <div v-if="errors.confirm_password"><span class="fieldName">Confirmed password</span> - {{errors.confirm_password}}</div>
                  <div v-if="errors.non_field_errors"> {{errors.non_field_errors}}</div>
                </v-alert>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="signUp" color="primary" flat v-bind:disabled="!valid">Sign up</v-btn>
            </v-card-actions>

          </v-card>
        </v-flex>
      </v-layout>
    </v-container>

  </div>
</template>

<script>
  import axios from 'axios'

  export default {
    name: "AppSignUp",
    data() {
      return {
        valid: false,
        username: '',
        email: '',
        password: '',
        confirm_password: '',
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
        showPassword: false,
        showConfirmPassword: false,
      }
    },
    methods: {
      signUp: function () {
        axios
          .post('./api/user/create/', {
            username: this.username,
            email: this.email,
            password: this.password,
            confirm_password: this.confirm_password,
          })
          .then(response => {
            console.log(response);
            document.location.href = '/';
            // this.$router.push('/');
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
