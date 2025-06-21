<template>
    <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading">Book Tickets </h3> <button @click="closeBooking" class="btn btn-dark new">Close</button></span>
            <div class="create-heading new3"> Booking {{ show.name }} at {{ show.theater_name }}</div>
            <div>Available Seats: {{ show.available }}</div>
            <div>Book Seats</div>
            <input type="number" v-model="seatsBooked" placeholder="Number of Seats" min="1" :max="show.available">

            <input type="text" v-model="ticket_price"  :disabled="true">
            <input type="number" v-model="totalAmount" placeholder="Total Amount" required :disabled="true">
            
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="BookTickets" class="create-button">Confirm Booking </button>
        </div>
        
    </div>

</template>
<script>
import axios  from "axios";
export default{
    name:'BookTickets',
    props:{
        show:{
            type:Object,
            required:true,
        }
    },
    emits:['closeBooking'],
    data(){
        return {
        message_f:'',
        message_s:'',
        errors:[],
        seatsBooked:null,
        ticket_price:'',
        }
    },
    mounted(){
        this.ticket_price=this.show.ticketPrice

    },
    components:{
    },
    computed:{
        totalAmount(){
            return (this.ticket_price*this.seatsBooked);
        }
    },
    methods:{
        BookTickets(){
            const data={
                'number':this.seatsBooked,
            }
            const token = localStorage.getItem('token')
            
            axios.post(`http://localhost:5000/api/user/book/${this.show.id}`,data,{
  headers: {
    'Content-Type': 'application/json',
    'Authorization': token
  },
}).then(response => {
            this.message_s=response.data.message
            setTimeout(() => {
         console.log("emitting close form !")
          this.$emit('closeBooking');
        }, 1000); 
        }).catch(error => {
            this.error=error.message;
        })

        },
        closeBooking(){
            this.$emit('closeBooking'); 
        },
        onImageChange(event){
            this.selectedFile=event.target.files[0];
        }
        ,
    }
}
</script>
<style scoped>
.create-page{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: #053544;
}
.create-form{
    max-width: 400px;
    padding: 20px;
    background-color: #fff;
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
  .new{
    display: inline-block;
    justify-content: right;

  }
  .new3{
    text-justify: left;
    justify-content: left;
    color:white
  }
</style>