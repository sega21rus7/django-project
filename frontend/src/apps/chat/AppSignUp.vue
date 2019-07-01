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
              <v-form v-model="valid">
                <v-text-field
                  :rules="[rules.required, rules.username]" clearable label="Login"
                  name="login" prepend-icon="person" required type="text" v-model="username">
                </v-text-field>
                <v-text-field :rules="rules.required" clearable label="Email" name="email"
                              prepend-icon="email" required type="text" v-model="email">
                </v-text-field>
                <v-text-field :append-icon="showPassword ? 'visibility' : 'visibility_off'" :rules="[rules.required, rules.password]"
                              :type="showPassword ? 'text' : 'password'" @click:append="showPassword = !showPassword"
                              clearable id="password" label="Password" name="password"
                              prepend-icon="lock" required
                              v-model="password">
                </v-text-field>
                <v-text-field :append-icon="showConfirmPassword ? 'visibility' : 'visibility_off'"
                              :rules="[rules.required, rules.password]" :type="showConfirmPassword ? 'text' : 'password'" @click:append="showConfirmPassword = !showConfirmPassword"
                              clearable id="confirm_password" label="Confirm password" name="password"
                              prepend-icon="lock" required
                              v-model="confirm_password">
                </v-text-field>
                <v-alert :value="true"
                         type="error"
                         v-if="errors"
                >
                  {{errors}}
                </v-alert>
              </v-form>
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn @click="signUp" color="primary">Sign up</v-btn>
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
          username: [
            v => v.length >= 5 || 'Login must be more than 8 characters or equal to 5'],
          password: [
            v => v.length >= 6 || 'Password must be more than 8 characters or equal to 6',
            v => v.length <= 32 || 'Password must be less than 32 characters or equal to 32',
          ],
        },
        // usernameRules: [
        //   v => !!v || 'Login field is required',
        //   v => v.length >= 5 || 'Login must be more than 8 characters or equal to 5',
        // ],
        // passwordRules: [
        //   v => !!v || 'Password field is required',
        //   v => v.length >= 6 || 'Password must be more than 6 characters or equal to 6',
        //   v => v.length <= 32 || 'Password must be less than 32 characters or equal to 32',
        // ],
        // emailRules: [
        //   v => !!v || 'Email field is required',
        // ],
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
      }
    }
  }
</script>

<style scoped>

</style>
