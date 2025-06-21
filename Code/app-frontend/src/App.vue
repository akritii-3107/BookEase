<template>
  <div id="app">
    <HeaderPage></HeaderPage>
    <RouterView></RouterView>
    <FooterPage></FooterPage>
  </div>
  
</template>
<script>
import HeaderPage from './components/Header.vue'
import FooterPage from './components/Footer.vue'
export default {
  name: 'App',
  components: {
    HeaderPage,
    FooterPage,
},
}
</script>
<style>
#app {
  font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
