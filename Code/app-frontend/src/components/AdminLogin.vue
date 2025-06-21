<template>
  <div class="login-page">
    <div class="login-form">
      <h2 class="login-heading">User Login</h2>
      <div>
        <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
        <input type="text" v-model="username" placeholder="Username" />
        <p v-if="username_error"  class="error">{{ username_error }}</p>
        <input type="password" v-model="password" placeholder="Password" />
        <p v-if="password_error"  class="error">{{ password_error }}</p>
        <button @click="login" class="login-button">Log in</button>
        <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
        <div class="login-form">
          <h6>Not Registered Yet ? Sign Up Now !</h6>
          <button class="new"><RouterLink to="/usersignup" class="text-white">Sign Up</RouterLink></button>
        
        </div>
      </div>
    </div>
  </div>

</template>

<script>
export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: '',
      username_error:'',
      password_error:'',
      message_f:'',
      message_s:'',
    };
  },
  methods: {
    login(event) {
      event.preventDefault();
      if(!this.username){
        this.username_error="Enter the username";
      }
      if(!this.password){
        this.password_error="Enter the Password";
              }
      if(this.username_error || this.password_error){
        return;
      }
      fetch('http://localhost:5000/api/login', {
method: 'POST',
headers: {
  'Content-Type': 'application/json'
},
body: JSON.stringify({
  username: this.username,
  password: this.password,
}),
}).then(response => {
        if(!response.ok){
          if(response.status === 401 ){
            return response.json().then(data => {
              this.message_f=data.message;
              throw new Error(data.message);
            });
          }
          else{
            throw new Error("Unexpected error occured")
          }
        }
          return response.json()
      }).then( data => {
        const token = data.token;
        localStorage.setItem('token',token);
        this.message_s="You are successfully Logged In";
        setTimeout(() => {
    this.$router.push('/dashboard');
        }, 3000); 

      }
      ).catch(error => { 
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
  background-color: #fafafa;
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
.text-white{
  text-decoration: none;

}
.new{
  background-color: #333;
}

input {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
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
</style>