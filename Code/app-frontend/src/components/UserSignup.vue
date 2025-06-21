<template>
    <div class="login-page">
      <div class="login-form">
        <h2 class="login-heading">User SignUp</h2>
        <div>
            <input type="email" v-model="email" placeholder="Email" />
            <p v-if="email_error"  class="error">{{ email_error }}</p>
          <input type="text" v-model="username" placeholder="Username" />
          <p v-if="username_error"  class="error">{{ username_error }}</p>
          <input type="password" v-model="password" placeholder="Password" />
          <p v-if="password_error"  class="error">{{ password_error }}</p>
          <input type="password" v-model="confirm_password" placeholder="Confirm Password" />
          <p v-if="confirm_password_error" class="error">{{ confirm_password_error}}</p>
          <button @click="signup" class="login-button">SignUp</button>
          <div v-if="error"  class="p-3 mb-2 bg-info-subtle text-emphasis-info">{{ error }}</div>
          <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
          <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
          <div class="login-form">
            <h6>Already Registered ? Login !</h6>
            <button class="new"><RouterLink to="/userlogin" class="text-white">Login</RouterLink></button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
//import axios from 'axios';

  export default {
    name: 'UserSignup',
    data() {
      return {
        username: '',
        password: '',
        email:'',
        username_error:'',
        error:'',
        email_error:'',
        password_error:'',
        confirm_password:'',
        confirm_password_error:'',
        message_s:'',
        message_f:'',

      };
    },
    methods: {
        isUsernameValid(){
            const pattern= /^[a-zA-Z0-9_]+$/;
            return pattern.test(this.username)

        },
      signup() {
        if (!this.username){
            this.username_error='Please Enter a username'
        }
        if (!this.email){
            this.email_error='Please Enter The email'
        }
        if (!this.password) 
        {
            this.password_error='Please enter the password'
        }
        if (!this.confirm_password) 
        {
            this.confirm_password_error='Please confirm the password'
        }
        if(this.password != this.confirm_password)
        {
            this.error='The password and Confirm password do not match'
            return;
        }
        if(this.username_error || this.password_error || this.email_error || this.confirm_password_error ){
            return;
        }
        if(!this.isUsernameValid || !this.username.length>=6){
            this.error='Invalid Username,must only contain letters, underscore and numbers and must be longer than 5 characters';
            return;
        }
        if(!this.password.length>=8){
            this.error=' The Password must atleast contain 8 chanacters'
            return;
        }
        console.log(this.username,this.password,this.email)
fetch('http://localhost:5000/api/register', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: this.email,
    username: this.username,
    password: this.password,
  }),
}).then(response => {
          if(!response.ok){
            if(response.status === 409 ){
              return response.json().then(data => {
                this.message_f=data.message;
                throw new Error(data.message);
              });
            }
            else{
              throw new Error("Unexpected error occured")
            }
          }
            response.json().then(data => {
              this.message_s=data.message
            })
            alert("You have registered Successfully")
            setTimeout(()=> {
              this.$router.push('/userlogin');
            },1000);
            
            
        }).catch(error => { 
            this.message_f=error.message;
        })
      },
    },
  };
  </script>
  
  <style>
  .login-page {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: #053544;
  }
  
  .login-form {
    max-width: 400px;
    padding: 20px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    text-align: center;
  }
  
  .login-heading {
    margin-bottom: 20px;
    color: #333;
  }
  
  input {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  .new{
    background-color: #333;
  }
  
  .login-button {
    width: 100%;
    padding: 10px;
    background-color: #3897f0;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  .text-white{
    text-decoration: none;

  }
  </style>
  