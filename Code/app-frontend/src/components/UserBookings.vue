<template>
    <div>
    <div class="special-section">
        <div class="special-section-content">
          <h2>Welcome, {{ user_name }}</h2>
          <div class="special-links">
            <span>  <button type="button" class="btn btn-dark btn-lg user-nav"><router-link to="/userprofile">Profile</router-link>
            </button>
            <button type="button" class="btn btn-dark btn-lg user-nav">
                <router-link to="/bookings">Bookings</router-link>
            </button> 
            <button type="button" class="btn btn-dark btn-lg user-nav">
                <router-link to="/dashboard">Dashboard</router-link>
            </button> </span>
          </div>
        </div>
      </div>
      <section class="shows">
          <div class="container text-center">
            <div class="row row-cols-1 row-cols-md-3 g-4">
              <div class="col" v-for="booking in bookings" :key="booking.show_id">
    <div class="card">
      <img :src="getImage(booking.image_path)" class="card-img-top" alt=".">
      <div class="card-body">
        <h5 class="card-title">{{ booking.show_name }} at {{ booking.theater_name }} {{ booking.booking_date }}</h5>
        <button class="btn btn-dark btn-lrg" @click="RateShow(booking.show_id)">Rate</button>
        <ReviewShow v-if="selected_show_id === booking.show_id && show_review" :booking="booking" @closeReview="closeReview"></ReviewShow>
      </div>
    </div>
  </div>

            </div>
          </div>
        </section>

</div>
  </template>
  
  <script>
  import ReviewShow from './ReviewShow.vue'

  export default {
    name:'UserBookings',
    data(){
        return {
            user_name:localStorage.getItem('username'),
            bookings:[],
            selected_show_id:null,
            show_review:false,
        }
    },
    components:{
    ReviewShow,
},
    mounted(){
      this.fetchBookings()
    },
    methods:{
      fetchBookings(){
            const token=localStorage.getItem('token')
            fetch('http://127.0.0.1:5000/api/user/bookings',{
                method: 'GET',
            headers: {
                'Authorization':token,
            },
            }).
            then(response => {
                if(!response.ok){
                    if(response.status === 404){
                        return response.json().then(data => {
                            this.message_f=data.message;
                            throw new Error("Theaters not found")
                        });
                    }
                    else{
                        throw new Error("Unexpected Error occured")
                    }
                }
                return response.json()
            })
            .then(data => {
                this.bookings=data
            })
            .catch(error => {
                console.error('Error fetching Bookings',error);
            })
      },
        getImage(imagePath){
            return `http://localhost:5000/api/theater-imgs/${imagePath}`

        },
        RateShow(show_id){
            console.log(show_id)
            this.selected_show_id=show_id
            this.show_review=true
        },
        closeReview(){
          this.selected_show_id=null,
          this.show_review=false
        }
        }
    }

  </script>
  
  <style>
  .special-section {
    background-image: url('../assets/section-bg.png');
    background-size: cover;
    background-position: center;
    height: 120px;
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    padding-bottom: 5px;
    padding-top: 8px;
    border-radius: 2px;
    border: solid black 2px ;
    display: flex;
    align-items: center;
    justify-content: left;
    color: white;
  }
  .special-section-2 {
    background-color:#053544;
    background-size: cover;
    background-position: center;
    height: 50px;
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    padding-bottom: 5px;
    padding-top: 8px;
    border-radius: 2px;
    border: solid black 2px ;
    display: flex;
    align-items: center;
    justify-content: left;
    color: white;
  }
  
  
  .special-section-content {
    text-align: center;
  }
  
  .special-links {
    margin-top: 20px;
  }
  
  .special-links a {
    color: white;
    text-decoration: none;
    margin-right: 20px;
  }
  .rest-bg{
    background-color: #0a6e7a;
  }
  .user-nav{
    padding: auto;
    border: 3px;
    margin: 3px;
  }
  .new{
    display: inline-block;
    justify-content: right;
    padding-bottom: 2px;
    padding-right: 5px;
    margin-bottom: 5px;
    margin-right: 5px;

  }
  .card-img-top img{
  object-fit: cover;

}
@media(min-width: 576px){
  .card-img-top{
    height: 46vw;;
  }
}
@media(min-width: 768px){
  .card-img-top{
    height: 70vw;
  }

}
@media (min-width: 992px){
  .card-img-top{
    height: 25vw;
  }  
}

  .new3{
    background-color: #000000;
  }

  </style>