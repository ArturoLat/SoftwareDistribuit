<template>
  <div id="app">
    <div class="title-container">
        <h1>Sport Matches</h1>
    </div>
    <div class="container">
      <div class="form-container" v-if="!creatingAccount">
        <h2 class="form-title">Sign In</h2>
        <div class="form-label-group">
          <label for="inputUsername">Username</label>
          <input type="text" id="inputUsername" class="form-control" placeholder="Username" required autofocus v-model="username">
        </div>
        <div class="form-label-group">
          <label for="inputPassword">Password</label>
          <input type="password" id="inputPassword" class="form-control" placeholder="Password" required v-model="password">
        </div>
        <div class="button-container">
          <button class="btn btn-primary" @click="checkLogin">Sign In</button>
          <button class="btn btn-success" @click="creatingAccount = true">Create Account</button>
          <button class="btn btn-secondary" @click="backToMatches">Back To Matches</button>
        </div>
      </div>
      <div class="form-container" v-else>
        <h2 class="form-title">Create Account</h2>
        <div class="form-label-group">
          <label for="createUsername">Username</label>
          <div class="input-group">
            <input type="text" id="createUsername" class="form-control" placeholder="Username" required v-model="addUserForm.username">
          </div>
        </div>
        <div class="form-label-group">
          <label for="createPassword">Password</label>
          <div class="input-group">
            <input type="password" id="createPassword" class="form-control" placeholder="Password" required v-model="addUserForm.password">
          </div>
        </div>
        <div class="button-container">
          <button class="btn btn-primary" @click="createAccount">Submit</button>
          <button class="btn btn-secondary" @click="creatingAccount = false">Back To Login</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'login',
  data () {
    return {
      logged: false,
      username: null,
      password: null,
      token: null,
      creatingAccount: false,
      addUserForm: {
        username: null,
        password: null
      }
    }
  },
  methods: {
    checkLogin () {
      const parameters = 'username=' + this.username + '&password=' + this.password
      const config = {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }
      const path = 'http://localhost:8000/login'
      axios.post(path, parameters, config)
        .then((res) => {
          this.logged = true
          this.token = res.data.access_token
          this.$router.push(
            {
              path: '/',
              query: {username: this.username, logged: this.logged, token: this.token}
            })
        })
        .catch((error) => {
          console.error(error)
          this.$alert('Username or Password incorrect')
        })
    },
    backToMatches () {
      this.$router.push({ path: '/' })
    },
    createAccount () {
      const accountData = {
        username: this.addUserForm.username,
        password: this.addUserForm.password
      }
      const path = 'http://localhost:8000/account/'

      axios.post(path, accountData)
        .then((res) => {
          this.addUserForm.username = ''
          this.addUserForm.password = ''
          this.$alert('Account created')
          this.creatingAccount = false
        })
        .catch((error) => {
          if (error.response && error.response.status === 404) {
            this.$alert('Error: Account already exists')
          } else {
            this.$alert('Error: Failed to create account')
          }
          console.log(this.addUserForm.username)
          console.error(error)
        })
    }
  },
  created () {
    this.logged = this.$route.query.logged === 'true'
    this.username = this.$route.query.username
    this.token = this.$route.query.token
    if (this.logged === undefined) {
      this.logged = false
    }
  }
}
</script>

<style scoped>
  .container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }

  .title-container{
  border-bottom: 2px solid black;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-right: 100px;
  padding-left: 100px;
  padding-bottom: 30px;
  background-color: white;

}

  .form-container {
  margin-top: 30px;
  padding: 50px;
  border: 1px solid black;
  background-color: white;
  width: 400px;
}

.form-label-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
}

.form-label-group label {
  margin-bottom: 8px;
  text-align: left;
}

.input-group {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.input-group input {
  flex: 1;
  padding: 8px;
  font-size: 14px;
}

.button-container {
  display: flex;
  flex-direction: column;
  margin-top: 16px;
}

.button-container button {
  width: 100%;
  margin-bottom: 8px;
  font-size: 14px;
}

body {
  background-color: beige;
}
</style>
