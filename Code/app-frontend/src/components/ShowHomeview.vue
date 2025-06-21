<template>
    <div>
  <div class="special-section">
    Show Details : {{ show.name }}
  </div>
<div class="rest-bg">
<div class="home-view">
  <section class="banner container-fluid">
    <hr>
    <img :src="getImage(show.image_path)" class=""> 
          <!-- Section 1: Show Title and Description -->
          <p>{{ show.description }}</p> 
  </section>
<hr>
<div class="show-details">
  <p>{{ show.description }}</p>
</div>
<hr>
  <div class="show-details">

    <section class="section">
      <!-- Section 2: Show Ratings and Tags -->
      <div>
        <p>Rating: {{ show.rating }}</p>
        <p>Tags: {{ show.tags }}</p>
        <p>Genre: {{ show.genre }}</p>
      </div>
    </section>

    <section class="section">
      <!-- Section 3: Show Schedule and Ticket Price -->
      <p>Schedule: {{ show.time }} - {{ show.date_s }}</p>
      <p>Ticket Price: {{ show.ticketPrice }}</p>
    </section>

<hr>
<div class="show-details">
  <p> Unbooked Seats : {{ show.available }}</p>
</div>
<hr>

    <section class="comments-ratings">
      <!-- Section 3: Show Rating and Comments -->
      <h6>Comments & Ratings</h6>
      <ul class="comments-list">
        <li v-for="(comment,index) in show.comments" :key="index" class="comment">
          <div class="user-info">
            <span class="rating">{{ comment[0] }} / 10</span>
          </div>
          <p class="comment-text">{{ comment[1] }}</p>
        </li>
      </ul>



    </section>




  </div>

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
name: 'show_view',
props:['show_id'],
setup(props){
    console.log(props.show_id)
},
data(){
    return {
        message_f:'',
        message_s:'',
        dates:null,
        show:{},

    }
},
mounted(){
    console.log(this.show_id)
    this.GetShow();
},
methods:{
    GetShow(){
        axios.get(`http://localhost:5000/api/show/${this.show_id}`)
        .then(response => {
            this.show=response.data;
        })
        .catch(error => {
            this.message_f=error.message;
        })
    },
    getImage(imagePath){
        return `http://localhost:5000/api/theater-imgs/${imagePath}`

    },
}

}

</script>
<style scoped>

.banner {
  width: 300px; 
  height: 300px; 
  position: relative;
  overflow: hidden;
}

.banner img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* This property maintains the aspect ratio while covering the container */
}
.comments-ratings {
  margin-top: 20px;
}

.comments-list {
  list-style: none;
  padding: 0;
}

.comment {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 5px;
}

.username {
  font-weight: bold;
}

.rating {
  color: #f39c12; /* Adjust colors as needed */
}

.comment-text {
  font-style: italic;
}

.show-details {
  background-color: #053544;
  background-size: cover; /* Adjust to 'contain' if needed */
  background-position: center;
  padding: 20px;
  color: #fff;
}

.show-details h2 {
  font-size: 24px;
  margin-bottom: 10px;
}

.show-details p {
  font-size: 16px;
  line-height: 1.5;
}
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

.section {
  margin-bottom: 20px;
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
