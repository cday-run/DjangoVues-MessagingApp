<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1,
  h2 {
    font-weight: normal;
  }
  ul {
    list-style-type: none;
    padding: 0;
  }
  li {
    display: inline-block;
    margin: 0 10px;
  }

  .btn {
    border-radius: 0 !important;
  }

  .card-footer input[type="text"] {
    background-color: #ffffff;
    color: #444444;
    padding: 7px;
    font-size: 13px;
    border: 2px solid #cccccc;
    width: 100%;
    height: 38px;
  }

  .card-header a {
    text-decoration: underline;
  }

  .card-body {
    background-color: #ddd;
  }

  .chat-body {
    margin-top: -15px;
    margin-bottom: -5px;
    height: 380px;
    overflow-y: auto;
  }

  .speech-bubble {
    display: inline-block;
    position: relative;
    border-radius: 0.4em;
    padding: 10px;
    background-color: #fff;
    font-size: 14px;
  }

  .subtle-blue-gradient {
    background: linear-gradient(45deg,#004bff, #007bff);
  }

  .speech-bubble-user:after {
    content: "";
    position: absolute;
    right: 4px;
    top: 10px;
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-left-color: #007bff;
    border-right: 0;
    border-top: 0;
    margin-top: -10px;
    margin-right: -20px;
  }

  .speech-bubble-peer:after {
    content: "";
    position: absolute;
    left: 3px;
    top: 10px;
    width: 0;
    height: 0;
    border: 20px solid transparent;
    border-right-color: #ffffff;
    border-top: 0;
    border-left: 0;
    margin-top: -10px;
    margin-left: -20px;
  }

  .chat-section:first-child {
    margin-top: 10px;
  }

  .chat-section {
    margin-top: 15px;
  }

  .send-section {
    margin-bottom: -20px;
    padding-bottom: 10px;
  }
</style>

<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-6 offset-3">

          <div v-if="!loading && sessionStarted" refs='chatBody' id="chat-container" class="card">

            <div class="card-header text-white text-center font-weight-bold subtle-blue-gradient">
              Share the chat link to invite new friends
            </div>

            <div class='card-body'>
              <div class='container chat-body'>
                <div v-for='message in messages' :key='message.id' class='row chat-section'>
                  <template v-if='username === message.user.username'>
                    <div class='col-sm-7 offset-3'>
                      <span class='card-text speech-bubble speech-bubble-user float-right text-white subtle-blue-gradient'>
                        {{ message.message }}
                      </span>
                    </div>
                    <div class='col-sm-2'>
                      <img class='rounded-circle' :src='`http://placehold.it/40/007bff/fff&text=${message.user.username[0].toUpperCase()}`' />
                    </div>
                  </template>
                  <template v-else>
                    <div class='col-sm-2'>
                      <img class="rounded-circle" :src="`http://placehold.it/40/333333/fff&text=${message.user.username[0].toUpperCase()}`" />
                    </div>
                    <div class='col-sm-7'>
                      <span class="card-text speech-bubble speech-bubble-peer float-left">
                        {{ message.message }}
                      </span>
                    </div>
                  </template>
                </div>
              </div>
            </div>
          

          <div class="card-footer text-muted">
              <form @submit.prevent='sendMessage'>
                <div class="row">
                  <div class="col-sm-10">
                    <input v-model='message' type='text' placeholder='Type a message' />
                  </div>
                  <div class="col-sm-2">
                    <button class="btn btn-primary">Send</button>
                  </div>
                </div>
              </form>
            </div>
          </div>



          <div v-else-if="!loading && !sessionStarted">

            <h3 class="text-center">Welcome to Messenger!</h3>
            <br />
            <p class="text-center">
              To start start a new chat session click the button below,
              and then you can invite your friends over to chat!
            </p>
            <br />
            <button @click="startChatSession" class="btn btn-primary btn-lg btn-block">Start Chatting</button>

          </div>


          <div v-else>

            <div class='loading'>
              <img src='../assets/hourglass.png' />
              <h5>Loading...</h5>
            </div>

          </div>


      </div>
    </div>
  </div>
</template>

<script>

const $ = window.jQuery
const axios = require('axios').default;

export default {
  data() {
    return {
      sessionStarted: false,
      messages: [],
      message: '',
      loading: true,
    }
  },

  created() {
    this.username = sessionStorage.getItem('username')
    if (this.$route.params.uri) {
      this.joinChat()
      this.connectToWebsocket()
    }
    setTimeout(() => { this.loading = false }, 2000)
  },

  updated() {
    const chatBody = this.$refs.chatBody
    if (chatBody) {
      chatBody.scrollTop = chatBody.scrollHeight
    }
  },

  methods: {
    startChatSession() {
      axios({
        method: 'post',
        url:'http://localhost:8000/api/chats/',
        headers: {
          'Authorization': `Token ${sessionStorage.getItem('authToken')}`,
        },
      })
      .then((response) => {
        console.log(response)
        this.sessionStarted = true
        this.$router.push(`/chats/${response.data.uri}/`)
      }, (error) => {
        console.log(error);
      })
    },

    sendMessage() {
      axios({
        method: 'post',
        url: `http://localhost:8000/api/chats/${this.$route.params.uri}/messages/`,
        headers: {
          'Authorization': `Token ${sessionStorage.getItem('authToken')}`,
        },
        data: {
          'message': this.message
        }
      })
      .then((response) => {
        // console.log(response);
        // this.messages.push(response.data)
        this.message = ''
      }, (error) => {
        console.log(error);
      })
    },

    //look into 'success param'
    joinChat() {
      const uri = this.$route.params.uri
      axios({
        method: 'patch',
        url: `http://localhost:8000/api/chats/${uri}/`,
        headers: {
          'Authorization': `Token ${sessionStorage.getItem('authToken')}`,
        },
        data: {
          username: this.username
        }
      })
      .then((response)=>{
        const user = response.data.people.find((person) => person.username === this.username)
        if (user) {
          this.sessionStarted = true
          this.loadChatHistory()
        }
      }, (error) => {
        console.log(error);
      })
    },

    loadChatHistory() {
      axios({
        method: 'get',
        headers: {
          'Authorization': `Token ${sessionStorage.getItem('authToken')}`,
        },
        url: `http://localhost:8000/api/chats/${this.$route.params.uri}/messages/`,
      })
      .then((response)=> {
        this.messages = response.data.messages
        setTimeout(() => {this.loading = false }, 2000)
      }, (error)=> {
        console.log(error);
      })
    },

    connectToWebsocket() {
      const ws = new WebSocket(`ws://localhost:8081/${this.$route.params.uri}`)
      ws.onopen = this.onOpen
      ws.onclose = this.onClose
      ws.onmessage = this.onMessage
      ws.onerror = this.onError
    },

    onOpen(event) {
      console.log('connected', event.data)
    },

    onClose(event) {
      console.log('disconnected', event.data)
      setTimeout(this.connectToWebsocket, 3000)
    },

    onMessage(event) {
      console.log(event.data)
      const message = JSON.parse(event.data)
      console.log(message)
      this.messages.push(message)
    },

    onError(event) {
      console.log('error occured', event.data)
    }
  }
}

</script>