<template>
    <nav class="navbar navbar-expand-lg  navbar-custom">
      
      <div class="container">
        <router-link to="/" class="navbar-brand">BookEase</router-link>

        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
          @click="toggleNavbar"
        >

          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse " :class="{ 'show': navbarOpen,'navbar-collapse-left':navbarOpen}" id="navbarNav">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item">
              <router-link to="/" exact active-class="active-link" class="nav-link">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" exact active-class="active-link" class="nav-link">About</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/contact" exact active-class="active-link" class="nav-link">Contact</router-link>
            </li>
            <li v-if="isLoggedIn === false" class="nav-item">
              <router-link to="/userlogin"  exact active-class="active-link" class="nav-link">Login</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link to="/logout" exact active-class="active-link" class="nav-link">Log out</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link to="/dashboard"  exact active-class="active-link" class="nav-link">Dashboard</router-link>
            </li>
          </ul>
 
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavbarPage',
    data() {
    return {
      navbarOpen: false, 
      logIn:false,
    };
  },
  mounted() {
    this.logIn = !!localStorage.getItem('token');
  },
  methods: {
    toggleNavbar() {
      this.navbarOpen = !this.navbarOpen; 
    },
  },
  computed:{
    isLoggedIn() {
      const token = localStorage.getItem('token');
      if(token){
        return true;
      }else {
        return false;
      }
    },
  }
  }
  </script>
  
  <style scoped>
  .navbar-collapse-left {
  position: fixed;
  top: 50px; 
  bottom: 0;
  z-index: 50;
  width: 200px;
  background-color: #020707;
  transition: left 1s ease; 
  padding-top: 20px;
  max-height: 300px;
  border-radius: 0 5px 10px 0;
  justify-content:left;
  justify-items: left;
}

.navbar-nav{
  justify-content: flex-start;
  justify-items: flex-start;
}
.navbar-brand{
  color: #0e9a99;
  display: flex; 
  padding-left: 20px;
  justify-content: flex-start;
}

.nav-link {
  text-decoration: none;
  color: #0e9a99; 
  padding: 10px;
  transition: color 0.3s; 
}
.nav-link:hover {
  color: #ffffff; 
}

.active-link {
  font-weight: bold; 
  color: #51cfee; 
}

.navbar-collapse-left.show {
  left: 0;
}
.navbar-custom{
  background-color: #020707;
}

.navbar-collapse-left .navbar-nav {
  flex-direction: column;
  
}

.navbar-collapse-left .navbar-toggler {
  display: none;
}
.new3{
    background-color: #16baba;
  }

@media (max-width: 991.98px) {
  .navbar-toggler {
    position: absolute;
    right: 15px;
    bottom: 15px;
    z-index: 1001;
    padding-top: 10px;
    justify-content:flex-start;
  }
  .navbar {
  display: flex; 
  justify-content: flex-start;
  }


  .navbar-collapse-left.show {
    left: 0;
  }

}
  </style>
  