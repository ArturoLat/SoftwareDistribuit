<template>
  <div id="app">
    <div class="main-container">
      <div class="title-container">
        <h1>
          <span> Sport Matches </span>
          <span v-if="isAdmin"> ADMIN MODE </span>
        </h1>
        <div class="button-container">
          <template v-if="logged">
            <div class="username-container">
              <img src="../../static/perfil.jpg" class="profile-image"/>
              <span class="username">{{ username }}</span>
            </div>
            <div class="username-container">
              <img src="../../static/stonks.jpg" class="profile-image"/>
              <span class="username"> {{ money_available }}</span>
            </div>
            <button class="btn btn-outline-primary" @click="is_showing_cart = !is_showing_cart">
              <span class="cartTotaltext">{{ cartTotalQuantity }}</span>
              <span class="button-text">Veure Cistella</span>
            </button>
            <button class="btn btn-outline-danger" @click="confirmLogOut">
              <span class="button-text">Log Out</span>
            </button>
          </template>
          <template v-else>
            <button class="btn btn-outline-primary" @click="is_showing_cart = !is_showing_cart">
              <span class="cartTotaltext">{{ cartTotalQuantity }}</span>
              <span class="button-text">Veure Cistella</span>
            </button>
            <button class="btn btn-outline-success" @click="logIn">
              <span class="button-text">Log In</span>
            </button>
          </template>
        </div>
      </div>

      <div class="container container-beige" v-if="matches.length > 0 && !is_showing_cart ">
        <div class="row mx-auto">
          <div class="card card-beige border-0" style="width: 20rem;" v-for="(match) in this.matches" :key="match.id">
            <div class="card-body">
              <img class="card-img-top" :src="match.url">
              <br>
              <h5>{{ match.competition.sport }} - {{ match.competition.category }}</h5>
              <h6>{{ match.competition.name }}</h6>
              <h6><strong>{{ match.local.name }}</strong> ({{ match.local.country }}) vs <strong>{{ match.visitor.name }}</strong> ({{ match.visitor.country }})</h6>
              <h6>{{ match.date.substring(0,10) }}</h6>
              <h6>{{ match.price }} &euro;</h6>
              <span> Entrades disponibles: {{match.total_available_tickets}}</span>
              <button class = "btn btn-success button-afegir" @click="addEventToCard(match)">Afegeix a la cistella</button>

            </div>

          </div>
        </div>
      </div>
      <div v-else class="cart-container">
        <h1 class="cart-title">Cart</h1>
        <div class="cart-table-container">
          <table v-if="matches_added.length > 0" class="cart-table">
            <thead>
              <tr>
                <th>Sport</th>
                <th>Competition</th>
                <th>Match</th>
                <th>Quantity</th>
                <th>Price(&euro;)</th>
                <th>Total(&euro;)</th>
                <th>Eliminar</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(order, index) in matches_added" :key="index">
                <td >{{ order.competition.sport }}</td>
                <td>{{ order.competition.name }}</td>
                <td>{{ order.local.name }} vs {{ order.visitor.name }}</td>
                <td>
                  <div @mouseover="showButtons = true" @mouseleave="showButtons = false">
                    <button class="btn btn-danger btn-sm" @click="decreaseTicket(order)" v-show="showButtons">
                      -
                    </button>
                    <span class="cantidad">{{ order.quantity }}</span>
                    <button class="btn btn-success btn-sm" @click="increaseTicket(order)" v-show="showButtons">
                      +
                    </button>
                  </div>
                </td>
                <td>{{ order.price }}</td>
                <td>{{ getOrderTotal(order) }}</td>
                <td>
                  <button class="btn btn-danger" @click="removeOrder(index)">
                    Eliminar entrada
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <p v-else>Your cart is currently empty.</p>
        </div>
        <div class="cart-buttons">
          <button class="btn btn-secondary" @click="is_showing_cart  = !is_showing_cart ">Enrere</button>
          <button class="btn btn-success" :disabled="matches_added.length <= 0" @click="finalizePurchase()">Finalitzar Compra</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'matches',
  data () {
    return {
      match_id: '',
      money_available: null,
      matches: [],
      matches_added: [],
      is_showing_cart: false,
      showButtons: false,
      username: null,
      logged: false,
      token: null,
      isAdmin: null,
      total_price: null
    }
  },
  methods: {
    confirmLogOut () {
      this.$confirm('Are you sure you want to log out?', 'Confirmation', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      })
        .then(() => {
          this.logOut()
        })
    },

    addEventToCard (match) {
      if (!this.logged) {
        this.$alert('Not Account Logged')
        return
      }
      const matchExistIndex = this.matches_added.findIndex((m) => m.id === match.id)
      if (matchExistIndex >= 0) {
        const existingMatch = this.matches_added[matchExistIndex]
        existingMatch.quantity++
      } else {
        const newMatch = {...match, quantity: 1}
        this.matches_added.push(newMatch)
      }
    },
    getMatches () {
      const pathMatches = 'http://localhost:8000/matches/'
      const pathCompetition = 'http://localhost:8000/competition/'

      axios.get(pathMatches)
        .then((res) => {
          var matches = res.data.filter((match) => {
            return match.competition.id != null
          })
          var promises = []
          for (let i = 0; i < matches.length; i++) {
            const promise = axios.get(pathCompetition + matches[i].competition.id)
              .then((resCompetition) => {
                if (resCompetition.data.competition) {
                  delete matches[i].competition.id
                  matches[i].competition = {
                    'name': resCompetition.data.competition.name,
                    'category': resCompetition.data.competition.category,
                    'sport': resCompetition.data.competition.sport
                  }
                }
              })
              .catch((error) => {
                console.error(error)
              })
            promises.push(promise)
          }
          Promise.all(promises).then((_) => {
            this.matches = matches
          })
        })
        .catch((error) => {
          console.error(error)
        })
    },
    addPurchase (parameters) {
      const path = 'http://localhost:8000/orders/'

      axios.post(path, parameters, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + this.token
        }
      })
        .then(() => {
          this.$alert('Order done')
        })
        .catch((error) => {
          if (error.response) {
            const statusCode = error.response.status
            const responseData = error.response.data
            if (statusCode === 404) {
              console.log(responseData.detail)
            } else if (statusCode === 401) {
              console.log('Unauthorized')
            } else {
              console.log('Server Error')
            }
          } else if (error.request) {
            console.log('No response from server')
          } else {
            console.log('Error')
          }
        })
    },
    initAccount () {
      const config = {
        headers: {
          'Accept-Type': 'application/json',
          'Authorization': 'Bearer ' + this.token
        }
      }

      const url = 'http://127.0.0.1:8000/account/'

      axios.get(url, config)
        .then((res) => {
          console.log('Account selected')
          this.money_available = res.data.available_money.toFixed(2)
          this.isAdmin = res.data.is_admin
        })
        .catch((error) => {
          console.log(error)
        })
    },
    finalizePurchase () {
      for (let i = 0; i < this.matches_added.length; i += 1) {
        const parameters = {
          username: this.username,
          match_id: this.matches_added[i].id,
          tickets_bought: this.matches_added[i].quantity
        }
        if (this.money_available >= this.total_price) {
          this.addPurchase(parameters)
          this.initAccount()
          this.matches_added = []
        } else {
          this.$alert('Not enough money')
        }
      }
    },
    getOrderTotal (order) {
      this.total_price = order.price * order.quantity
      return this.total_price.toFixed(2)
    },
    removeOrder (index) {
      this.matches_added.splice(index, 1)
    },
    increaseTicket (order) {
      order.quantity++
    },
    decreaseTicket (order) {
      if (order.quantity > 1) {
        order.quantity--
      }
    },
    getAccount () {
      this.logged = this.$route.query.logged === 'true'
      this.username = this.$route.query.username
      this.token = this.$route.query.token
      if (this.logged === undefined) {
        this.logged = false
      }

      // Utiliza las variables como necesites
      console.log(this.username, this.logged, this.token)
      if (this.logged) {
        this.initAccount()
        this.getMatches()
      }
    },
    logIn () {
      this.$router.push('/userlogin')
    },
    logOut () {
      this.logged = false
      this.username = null
      this.token = null
    }
  },
  created () {
    this.getMatches()
    this.logged = this.$route.query.logged === 'true'
    this.username = this.$route.query.username
    this.token = this.$route.query.token
    if (this.logged === undefined) {
      this.logged = false
    }
  },
  mounted () {
    this.getAccount()
  },
  computed: {
    cartTotalQuantity () {
      let total = 0
      for (const order of this.matches_added) {
        total += order.quantity
      }
      return total
    }
  }
}

</script>

<style>
.title-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 100px 30px;
  background-color: white;
}

.title-container h1 {
  margin: 0;
}

.title-container .button-container {
  display: flex;
  gap: 10px;
}

body {
  background-color: beige;
}

.card {
  margin: 20px;
}

.card-body{
  background-color: white;
  padding: 0px 0px 40px;
}

.card-img-top {
  padding-bottom: 20px;
  width: 100%;
  height: auto;
}

.cart-container {
  text-align: center;
  margin: auto;
  width: 80%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px;
}

.cart-table-container {
  padding: 10px;
  border-radius: 5px;
  overflow-x: auto;
}

.cart-table {
  margin: auto;
  width: 100%;
  border-collapse: collapse;
}

.cart-title {
  font-size: 24px;
}

.cart-buttons {
  margin-top: 20px;
}

.username-container {
  display: flex;
  align-items: center;
}

.profile-image {
  width: 40px;
  height: 40px;
  margin-right: 10px;
}

.username {
  font-weight: bold;
  font-size: small;
}

.cartTotaltext{
  background-color: #007bff;
  color: white;
  padding: 5px;
  border: 1px solid #007bff;
  border-radius: 5px;
}

.main-container {
  display: grid;
  grid-template-rows: auto 1fr;
  grid-gap: 20px;
  align-items: start;
}
</style>
