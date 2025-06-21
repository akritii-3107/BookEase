<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
      <div class="container">
        | <router-link to="/" class="navbar-brand">Welcome {{ username }}</router-link>
        <form class="d-flex" role="search">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success" type="submit">Search</button>
      </form>
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
              <router-link to="/" class="nav-link" @click="toggleNavbar">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/about" class="nav-link" @click="toggleNavbar">About</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/contact" class="nav-link" @click="toggleNavbar">Contact</router-link>
            </li>
            <li v-if="isLoggedIn === false" class="nav-item">
              <router-link to="/userlogin" class="nav-link" @click="toggleNavbar">User Login</router-link>
            </li>
            <li v-if="isLoggedIn === false" class="nav-item">
              <router-link to="/adminlogin" class="nav-link" @click="toggleNavbar">Admin Login</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link to="/profile" class="nav-link" @click="toggleNavbar">Profile</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link to="/bookings" class="nav-link" @click="toggleNavbar">Bookings</router-link>
            </li>
            <li v-if="isLoggedIn" class="nav-item">
              <router-link to="/logout" class="nav-link" @click="toggleNavbar">Log out</router-link>
            </li>
          </ul>
 
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'NavbarUser',
    data() {
    return {
      navbarOpen: false, 
      logIn:false,
      username:''
    };
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
  top: 56px; 
  left: -250px;
  bottom: 0;
  z-index: 1000;
  width: 200px;
  background-color: #343a40;
  transition: left 1s ease; 
  padding-top: 20px;
  max-height: 300px;
  border-radius: 0 5px 10px 0
}

.navbar-collapse-left.show {
  left: 0;
}

.navbar-collapse-left .navbar-nav {
  flex-direction: column;
}

.navbar-collapse-left .navbar-toggler {
  display: none;
}

@media (max-width: 991.98px) {
  .navbar-toggler {
    position: absolute;
    right: 15px;
    bottom: 15px;
    z-index: 1001;
    padding-top: 10px
  }


  .navbar-collapse-left.show {
    left: 0;
  }
}
  </style>