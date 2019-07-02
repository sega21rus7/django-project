<template>
  <div>

    <v-layout row>
      <v-flex xs6>

      </v-flex>
      <v-flex xs6>
        <v-card>
          <v-toolbar color="pink" dark>
            <v-toolbar-title>Chat messages</v-toolbar-title>
            <v-spacer></v-spacer>
            <v-btn icon>
              <v-icon>search</v-icon>
            </v-btn>
          </v-toolbar>

          <v-list
            class="scroll-y"
            style="height: 400px;">
            <div v-for="item in message_list.results">
              <v-list-tile :key="item.id">
                <v-list-tile-content>
                  <v-list-tile-sub-title class="text--primary">{{ item.sender.username }}</v-list-tile-sub-title>
                  <v-list-tile-sub-title>{{ item.message }}</v-list-tile-sub-title>
                </v-list-tile-content>
                <v-list-tile-action>
                  <v-list-tile-action-text>{{ item.pub_date }}</v-list-tile-action-text>
                </v-list-tile-action>
              </v-list-tile>
            </div>
          </v-list>
        </v-card>
        <div class="text-xs-center">
          <v-pagination
            :length="pageCount"
            @input="switchPage"
            circle
            v-model="pageNumber"
          ></v-pagination>
        </div>
        <v-form @submit.prevent="sendMessage" v-model="valid">
          <v-text-field
            :rules="messageRules"
            clearable
            label="Type a message"
            required
            type="text"
            v-model="message"
          >
          </v-text-field>
          <v-btn @click="sendMessage" block color="green" dark>Send a message</v-btn>
        </v-form>

      </v-flex>
    </v-layout>


  </div>
</template>
<!--            autofocus-->
<script>
  export default {

    name: "AppChat",
    data() {
      return {
        valid: false,
        pageNumber: 1,
        message_list: {
          results: [],
          count: 0
        },
        message: '',
        messageRules: [
          v => !!v || 'Message field is required',
        ],
      }
    },
    mounted() {
      this.updateMessageList();
      setInterval(this.updateMessageList, 1000)
    },
    computed: {
      pageCount() {
        if (this.message_list === null) {
          return 0
        }
        return Math.ceil(this.message_list.count / 10)
      }
    },
    methods: {
      sendMessage: function () {
        this.createMessage();
        this.message = '';
        // this.updateMessageList();
      },
      createMessage: function () {
        axios
          .post('./api/chat_message/create/', {
            message: this.message,
          })
          .then(response => console.log(response))
          .catch(error => console.log(error)
          );
      },
      updateMessageList: function () {
        axios
          .get("./api/chat_message/select/?page=" + this.pageNumber)
          .then(response => (this.message_list = response.data))
          .catch(error => console.log(error));
      },
      switchPage: function () {
        this.updateMessageList();
      }
    }
  }
</script>

<style scoped>

</style>
