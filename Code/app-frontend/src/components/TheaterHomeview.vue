<template>
        <div>
      <div class="special-section">
        Theater : {{ theater.name }},{{ theater.city }}
      </div>
  <div class="rest-bg">
    <div class="home-view">
      <section class="banner container-fluid">
        <img :src="getImage(theater.image_path)">  
      </section>
  <hr>
      <section class="upcoming-shows">
        <h2>Upcoming Shows</h2>
        <div>
    <div id="carouselExampleIndicators" class="carousel slide" data-bs-ride="true">    
  <div class="carousel-inner">
    <div class="carousel-item" v-for="show in theater.shows" :key="show.id" :class="getClassForItem(show.id)">
      <img :src="getImage(show.image_path)" class="special" alt="...">
      <hr>
      <div class="caption">
        <h5>{{ show.name }}</h5>
        <p>On {{ show.date }} at {{ show.time }}</p>
      </div>
    </div>
  </div>
  <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
  </button>
  <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
  </button>
</div>
  </div>
  <hr>


      </section>
  
      <section class="about-theatre">
        <h3>About the Theatre</h3>
        <h5>{{ theater.description }}</h5>
      </section>
      <hr>
      <hr>
    </div>
      <div>{{ message_f }}</div>
    </div>
</div>

  </template>
  
  <script>
  import axios from 'axios';
  export default {
    name: 'theater_view',
    props:['theater_id'],
    setup(props){
        console.log(props.theater_id)
    },
    data(){
        return {
            message_f:'',
            message_s:'',
            dates:null,
            theater:{},
            selectedShow:null

        }
    },
    mounted(){
        console.log(this.theater_id)
        this.GetTheater();
    },
    methods:{
        GetTheater(){
            axios.get(`http://localhost:5000/api/theater/${this.theater_id}`)
            .then(response => {
                this.theater=response.data;
                const randomIndex=Math.floor(Math.random()*this.theater.shows.length)
                this.selectedShow=this.theater.shows[randomIndex].id
            })
            .catch(error => {
                this.message_f=error.message;
            })
        },
        getImage(imagePath){
            return `http://localhost:5000/api/theater-imgs/${imagePath}`

        },
        getClassForItem(key){
            return {
                active: key === this.selectedShow
            }
           
        }
    }

  }

  </script>
  <style scoped>
    .special-section {
    background-image: url('../assets/section-bg.png');
    background-size: cover;
    background-position: center;
    height: 80px;
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
    padding-bottom: 5px;
    padding-top: 8px;
    border-radius: 2px;
    border: solid black 2px ;
    padding-left: 10px;
    display: flex;
    align-items: center;
    justify-content: left;
    color: white;
    font-size: 30px;
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
    color: aliceblue;
    padding-bottom: 50px;
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
.special{
    height: 300px;
    width: 300px;
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
  </style>
  