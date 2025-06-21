<template>
    <div></div>
        <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading"> Review Show</h3> <button @click="closeReview" class="btn btn-dark new">Close</button></span>
            <h5>Name : {{ this.booking.show_name }}</h5>
            <input type="number" min="1" max="10" v-model="showRating" placeholder="Rating(1-10)" required>
            <input type="text" v-model="comment" placeholder="Comment" >
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="RateShow" class="create-button btn btn-dark new">Submit Review</button>
        </div>
        
    </div>

</template>
<script>
import axios from 'axios';
export default{
    name:'RateShow',
    props:{
        booking:{
            type:Object,
            required:true,
        }
    },
    emits: ['closeReview'],
    data(){
        return {
            message_f:'',
            message_s:'',
            showRating:'',
            comment:'',
        };
    },
    computed:{
    },
    mounted(){
    },
    methods:{
        RateShow(){
            if(!this.showRating){
                this.message_f="Enter the Rating"
            }
            const data={
                'rating':this.showRating,
                'comment':this.comment
            }
            const token =localStorage.getItem('token')
            axios.post(`http://localhost:5000/api/user/rate/${this.booking.show_id}`,data,{
  headers: {
    'Authorization': token
  }
}).then( response => {
    if(response.status === 200){
        this.message_f=response.data.message
    }
    else{
        this.message_s=response.data.message
        this.$emit('closeReview')
    }
}
).catch(error => {
            this.message_f=error.message
        })
        }
        ,
        closeReview(){
            this.$emit('closeReview');
        },
    }
}
</script>
<style>
.create-page{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #053544;
}
.new{
    display: inline-block;
    justify-content: right;
    color: #fff;

  }
.delete-theater{
  padding-top: 10px;
  padding-bottom: 10px;
  border-radius: 4px;
  border-color: black;
  border: 5px 5px 5px 5px;

}
  .user-nav{
    padding: auto;
    border: 3px;
    margin: 3px;
  }
.create-form{
    max-width: 400px;
    padding: 20px;
    background-color: #fff;
    color: black;
    border: 1px solid #ddd;
    border-radius: 4px;
    text-align: center;

}
.create-heading{
    margin-bottom: 20px;
    color: #333;
    justify-content: left;
    display: inline-block;
}
.create-button {
    width: 100%;
    padding: 10px;
    background-color: #3897f0;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

</style>