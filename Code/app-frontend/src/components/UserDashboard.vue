<template>
    <div>
      <div class="special-section">
        <div class="special-section-content">
          <h2>Welcome, {{ user_name }}</h2>
          <div class="special-links">
            <span>            <button type="button" class="btn btn-dark btn-lg user-nav">
                <router-link to="/userprofile">Profile</router-link>
            </button>
            <button type="button" class="btn btn-dark btn-lg user-nav">
                <router-link to="/bookings">Bookings</router-link>
            </button> 
            <button @click="getLocation" v-if="!curr_location" class="btn btn-dark  btn-lg user-nav">Get current Location</button></span>
 
          </div>
        </div>
      </div>
      <div class="special-section-2">
        <div class="special-section-content">
          <div class="d-flex">
        <input class="form-control me-2" type="search" v-model="searchQuery" placeholder="Search for Shows,Rating,Genre,Tags" aria-label="Search">
        <button class="btn btn-dark new3"  @click="searchShows">Search</button>  <span class="space"> <input type="date" v-model="searchDate"></span> 
          </div>
          </div>
        </div>
  <div class="rest-bg">
    <button @click="getAll" v-if="curr_location" class="btn btn-dark  btn-lg user-nav">Nearest Shows (30 km ) ,See All </button>
      <div class="container">
        <div class="theaters">
          <div class="theater-creation">
        <div>
      </div>
      <div class="theater-list">
        <div v-for="show in filtered_shows" :key="show.id" class="theater-card">
          <router-link class="new5" :to="{name:'theater_view',params:{theater_id : show.theater_id}}">
            <h4>{{ show.theater_name }},{{ show.city }}</h4>
          </router-link>
          <div class="show-list">
            <div class="container text-center">
              <hr>
              <div class="row">
                <img class="col-3 theater-image show-img" :src="getImage(show.image_path)">
                <div class="col-6"> <router-link class="new5" :to="{name:'show_view',params:{show_id:show.id}}"> <h2>{{ show.name }} </h2> </router-link><hr>
                  <div class="table-container">
                    <div class="table-row">
                      <div class="table-cell new3">Starting</div>
                    <div class="table-cell">{{ show.date_s }}</div>
                    </div>
                    <div class="table-row">
                      <div class="table-cell new3">Time </div>
                    <div class="table-cell">{{ show.time }} onwards</div>
                    </div>
                    <div class="table-row">
                      <div class="table-cell new3">Genre</div>
                    <div class="table-cell">{{ show.genre }}</div>
                    </div>
                  </div>
                </div> 
                <div class="col-3">
                  <hr>
                  <button class="btn btn-dark btn-lg" v-if="show.availability" @click="BookShow(show)">Book Tickets</button>
                  <p v-if="show.availability">Available : {{ show.available }}</p>
                  <button class="btn btn-dark btn-lg" v-if="!show.availability" :disabled="true">HOUSE FULL</button>
                  <hr>
                  <button type="button" :class="getfillingFast(show.filling_fast)">Filling Fast</button>
                </div>
              </div>
              <div v-if="select_show_id_book && show.id === select_show_id_book" class="row">
              <BookTickets :show="show" @closeBooking="closeBooking"></BookTickets></div>
                <hr>
</div>
          </div>
      </div>
    </div>
        </div>
        </div>
      </div>
      <div>{{ message_f }}</div>
    </div>
</div>
  </template>
  
  <script>
  import { getDistance } from 'geolib';
  import BookTickets from './BookTickets.vue'
  export default {
    name:'UserDashboard',
    data(){
        return {
            user_name:localStorage.getItem('username'),
            shows:[],
            curr_location:false,
            filtered_shows:[],
            tags_search:'',
            rating_search:'',
            searchQuery:'',
            searchDate:'',
            maxDistance:30.0,
            showData:{},
            user_latitude:'',
            user_longitude:'',
            select_show_id_detail:null,
            select_show_id_book:null,
            moredetails:false,

        }
    },
    components:{
      BookTickets,
    },
    watch:{
      searchQuery(newValue){
        if(newValue === ''){
          this.fetchShows();
        }
      },
      searchDate:'searchbyDate',
      },
    mounted(){
      this.fetchShows()
    },
    created(){
      this.interval=setInterval(() => {this.fetchShows();
      }, 80000);
    },
    beforeUnmount(){
      clearInterval(this.interval);
    },
    methods:{
      fetchShows(){
        this.searchDate='';
            fetch('http://127.0.0.1:5000/api/shows',{
                method: 'GET',
            headers: {
                'Content-Type': 'application/json'
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
                this.shows=data
                this.filtered_shows=data
            })
            .catch(error => {
                console.error('Error fetching Shows',error);
            })
        },
        getImage(imagePath){
            return `http://localhost:5000/api/theater-imgs/${imagePath}`

        },
        getLocation(){
            if(navigator.geolocation){
                this.curr_location=true
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        this.user_latitude=position.coords.latitude;
                        this.user_longitude=position.coords.longitude;
                        this.findNearbyTheaters();
                    },
                    (error) => {
                        switch(error.code){
                            case error.PERMISSION_DENIED:
                                this.message_f="Location Permision denied";
                                break;
                            case error.POSITION_UNAVAILABLE:
                                this.message_f="Current Location not available";
                                break;
                            default:
                                this.message_f="Could not get Location, some error occured";
                                break;
                              }
                    }
                )
            }
            else{
                this.message_f="GeoLocation is not supported by your browser";
            }
        },
        findNearbyTheaters(){
          this.filtered_shows=this.filtered_shows.filter(
            show => {
              console.log(show.lat,show.long)
              const distance = getDistance(
                {latitude:parseFloat(this.user_latitude),
                longitude:parseFloat(this.user_longitude)},
                {
                  latitude:parseFloat(show.lat),
                  longitude:parseFloat(show.long)
                });
                console.log(distance)
                const distanceInKilometers = distance/ 1000;
                console.log(distanceInKilometers)
                return distanceInKilometers <= this.maxDistance;});
            console.log(this.filtered_shows)
            },
            getAll(){
              this.curr_location=false;
              this.fetchShows();
            },
            searchShows(){
              if(this.searchQuery.trim() === ''){
                return;
              }
              this.filtered_shows=this.filtered_shows.filter((show) => {
                const query=this.searchQuery.trim().toLowerCase();
                for (const key in show){
                  if(typeof show[key] === 'string' && show[key].toLowerCase().includes(query)){
                    return true;
                  }
                }
                return false;
              })
            },
            sortByRating(){
              this.filtered_shows.sort((a,b)=> parseInt(b.rating)>parseInt(a.rating))
            },
            toggleMoreDetails(){
              this.moredetails=!this.moredetails;
            },
            BookShow(show){
              this.select_show_id_book=show.id
              
            },
            closeBooking(){
              this.select_show_id_book=null
              this.fetchShows()
            },
            searchbyDate(){
              clearTimeout(this.timeout);
              this.timeout = setTimeout(()=>{
                if(this.searchDate){
              this.filtered_shows=this.shows
              const date = new Date(this.searchDate);
              const formattedDate = date.toLocaleDateString('en-GB');
              this.filtered_shows=this.filtered_shows.filter((show) => {
                return show.date_s === formattedDate
              });
              console.log(this.filtered_shows)
              }
              },800);


            },
            getfillingFast(availability){
              return availability ? 'btn btn-success' : 'btn btn-secondary';
            },
            simpleclass(){
              return "btn"
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
    height: 80px;
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
  
  .green{
    background-color: green;
    color: aliceblue;
  }

  .gray{
    background-color: gray;
    color: aliceblue;
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

  .new3{
    background-color: #000000;
  }
  .space{
    padding-left: 5px;
    padding-right: 5px;
    margin-left: 5px;
    margin-right: 5px;
  }
  .new5{
    color: #ffffff;
    text-decoration: none;
  }
  .new5:hover{
    color: aquamarine;
  }

  </style>
  