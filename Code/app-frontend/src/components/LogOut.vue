<template>
    <div class="logout-page">
      <p>Are you sure you want to logout?</p>
      <button class="btn btn-dark" @click="logout">Logout</button>
    </div>
  </template>
  
  <script>
  export default {
    name:'LogOut',
    methods: {
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('username')
        setTimeout(() => {
          location.reload();
          window.location.href='/'
        }, 1000); 
      },
    },
  };
  </script>
  <style>
  .logout-page{
    background-color: #053544;
    justify-content: center;
    padding-top: 200px;
    justify-items: center;
    color: white;
    height: 100vh;
    object-fit: cover;
  }
</style>
  