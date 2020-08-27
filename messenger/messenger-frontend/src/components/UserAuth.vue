<style scoped>
    #auth-container {
        margin-top: 50px;
    }

    .tab-content {
        padding-top: 20px;
    }
</style>

<template>
  <div class='container py-1'>
    <h1 class='text-center'>Welcome to Django Vues!</h1>
    <h5 class='text-center'>A Chat App Made with Django and Vue.js</h5>
    <div id='auth-container' class='row'>
      <div class='col-sm-4 offset-sm-4'>
        <ul class='nav nav-tabs nav-justified' id='myTab' role='tablist'>
          <li class='nav-item'>
            <a class='nav-link active text-success' id='signup-tab' data-toggle='tab' href='#signup' role='tab' aria-controls='signup' aria-selected='true'>Sign Up</a>
          </li>
          <li class='nav-item'>
            <a class='nav-link text-success' id='signin-tab' data-toggle='tab' href='#signin' role='tab' aria-controls='signin' aria-selected='false'>Sign In</a>
          </li>
        </ul>
        <div class='tab-content' id='myTabContent'>
          <div class='tab-pane fade show active' id='signup' role='tabpanel' aria-labelledby='signin-tab'>
            <form @submit.prevent='signUp'>
              <div class='form-group'>
                <input v-model='email' type='email' class='form-control' id='email' placeholder='Email Address' required>
              </div>
              <div class='form-row'>
                <div class='form-group col-md-6'>
                  <input v-model='username' type='text' class='form-control' id='username' placeholder='Username' required>
                </div>
                <div class='form-group col-md-6'>
                  <input v-model='password' type='password' class='form-control' id='password' placeholder='Password' required>
                </div>
              </div>
              <button type='submit' class='btn btn-block btn-success'>Sign up</button>
              <div v-if='error != null' class='error-message'>
                <div v-for='item in error'>
                  <li class='py-1 text-light'>
                    {{ item }}
                  </li>
                </div>
              </div>
            </form>
          </div>
          <div class='tab-pane fade' id='signin' role='tabpanel' aria-labelledby='signin-tab'>
            <form @submit.prevent='signIn'>
              <div class='form-group'>
                <input v-model='username' type='text' class='form-control' id='username' placeholder='Username' required>
              </div>
              <div class='form-group'>
                <input v-model='password' type='password' class='form-control' id='password' placeholder='Password' required>
              </div>
              <button type='submit' class='btn btn-block btn-success'>Sign in</button>
            </form>
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
  data () {
    return {
      email: '', 
      username: '', 
      password: '',
      error: null
    }
  },
  methods: {
    signUp () {
      const email = document.querySelector('#email').value;
      const username = document.querySelector('#username').value;
      const password = document.querySelector('#password').value;
      axios({
        method: 'POST',
        url: 'http://127.0.0.1:8000/auth/users/',
        data: {
          'username': username,
          'email': email,
          'password': password
        }
      })
      .then((response) => {
        console.log(response)
        this.signIn()
      })
      .catch ((error) => {
        console.log(error.response.data.password);
        this.error = error.response.data.password
      })
    },
    signIn () {
      const username = document.querySelector('#username').value;
      const password = document.querySelector('#password').value;
      axios({
        method: 'post',
        url: 'http://localhost:8000/auth/token/login/',
        data: {
          username: username,
          password: password
        }
      })
      .then((response) => {
        console.log(response.data);
        sessionStorage.setItem('authToken', response.data.auth_token)
        sessionStorage.setItem('username', username)
        console.log(sessionStorage)
        this.$router.push('/chats')
      }, (error) => {
        console.log(error);
      })

      // const credentials = {username: this.username, password: this.password}
      // $.post('http://localhost:8000/auth/jwt/create/', credentials, (data) => {
      //   sessionStorage.setItem('authToken', data.token)
      //   sessionStorage.setItem('username', this.username)
      //   this.$router.push('/chats')
      // })
      // .fail((response) => {
      //   alert(response.responseText)
      // })
    },
    logout() {
      axios({
        method: 'post',
        url: 'http://localhost:8000/auth/token/logout/',
        headers: {
          'Authorization': `Token ${sessionStorage.getItem('authToken')}`,
        }
      })
      .then((response) => {
        console.log(response);
      }, (error) => {
        console.log(error);
      })
    }
  }
};

</script>


