<template>
    
    <div>
      <div class="user-profile">
        <h2>Welcome, {{ username }}</h2>
        <p>Email: {{ email }}</p>
        <button class="btn btn-dark" v-if="!this.disp_format" @click="ChangeFormat">Change Monthly Report Format</button>
        <button class="btn btn-dark" v-if="this.disp_format" @click="ChangeFormat">Close Format Form</button>
        <ReportFormat v-if="this.disp_format"></ReportFormat>
      </div>
    </div>
    <div class="bg">
        <img src="../assets/bookease-logo.png" alt="">
</div>
  </template>
  
  <script>
  import axios from 'axios';
  import ReportFormat from './ReportFormat.vue';
  
  export default {
    name: 'UserProfile',
    data() {
        return {
            username: '',
            email: '',
            disp_format:false,
        };
    },
    mounted() {
        this.fetchUserData();
    },
    methods: {
        fetchUserData() {
            const token = localStorage.getItem('token');
            axios.get('http://localhost:5000/api/user/profile', {
                headers: {
                    'Authorization': token,
                }
            })
                .then((response) => {
                this.username = response.data.username;
                this.email = response.data.email;
            })
                .catch((error) => {
                console.error('Error fetching user data:', error);
            });
        },
        ChangeFormat() {
            this.disp_format = !this.disp_format;
        }
    },
    components: { ReportFormat }
};
  </script>
  
  <style>
  .user-profile {
    background-color: #053544;
    color: azure;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  .bg{
  display: flex;
  justify-content: center;
  align-items: center;
  background-color:#053544;

  }
  .bg img{
    max-width: 100%;
  max-height: 100%;
  object-fit: cover; 

  }
  </style>
  