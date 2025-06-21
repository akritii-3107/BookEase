<template>
    <div>
      <main class="main">
        <section class="main-top">
          <div class="container">
            <h1>Welcome to BookEase</h1>
            <p>Explore Shows, Book Your Tickets and Enjoy ! </p>
          </div>
        </section>
        <section class="shows">
          <div class="container text-center">
            <div class="row row-cols-1 row-cols-md-3 g-4">
              <div class="col" v-for="show in shows" :key="show.id">
    <div class="card">
      <img :src="getImage(show.image_path)" class="card-img-top" alt=".">
      <div class="card-body">
        <h5 class="card-title">{{ show.name }}</h5>
      </div>
    </div>
  </div>

            </div>
          </div>
        </section>

        <section class="locations">
          <div class="container">
            <h2>We are currently available in </h2>
            <div class="location-cards">
            <div v-for="location in locations" :key="location" class="location-card">
              <div class="location-icon">
                <i class="fas fa-map-marker-alt"></i>
                <FontAwesomeIcon icon="map-marker-alt" />
              </div>
              <div class="location-details">
                <h3>{{ location }}</h3>
              </div>
              </div>
            </div>
          </div>
        </section>

        
      </main>
    </div>
  </template>
  
  <script>
 import { library } from '@fortawesome/fontawesome-svg-core';
import { faMapMarkerAlt } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

library.add(faMapMarkerAlt);
import axios from 'axios';
  
  export default {
    data(){
        return{
            locations:[],
            shows:[]
        }
    },
    name:'LandingPage',
    components:{
        FontAwesomeIcon,
    },
    created(){
        this.fetchCities();
        this.fetchShows();
    },
    methods:{
        fetchCities(){
            axios.get('http://127.0.0.1:5000/api/theaters/cities/').
            then(response => {
                this.locations=response.data;
            })
            .catch(error => {
                console.error('Error fetching Locations',error);
            })

        },
        fetchShows(){
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
            })
            .catch(error => {
                console.error('Error fetching Theaters',error);
            })

        },
        getImage(imagePath){
            return `http://localhost:5000/api/theater-imgs/${imagePath}`

        }
        
    }
  }
  </script>
  <style scoped>
  .main{
    background-color: #173e42;
  }
  .main-top{
    padding-top: 50px;
    color: #f9f9f9;
  }

.locations {
  text-align: center;
  padding: 40px 0;
  color: #ffffff;
}

.location-cards {
  display: flex;
  justify-content: center;
  color: black;
  flex-wrap: wrap;
  margin-top: 20px;
}

.img-bg{
    width: 200cqmax;
    height: 80cqmin;
    display: flex;
    justify-content: center;
    align-items: center;
}
.show-img {
  max-width: 100%;
}
.show-img img {
  max-width: 100%;
  height: auto;
}
.location-card {
  width: 250px;
  background-color: #f9f9f9;
  border-radius: 10px;
  margin: 10px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.location-icon {
  font-size: 24px;
  margin-right: 10px;
  color: #098CA6;
}

.location-details {
  text-align: left;
}
.btn-primary{
    margin-left: 10px;

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
</style>
  