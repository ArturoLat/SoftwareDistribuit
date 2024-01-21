<template>
  <div id="app">
    <router-view/>
    <footer class="footer"> MADE BY: Arturo and Zijian</footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: beige;
}

.footer{
  background-color: white;
  padding: 20px;
  text-align: center;
  margin-top: auto;
}

</style>
