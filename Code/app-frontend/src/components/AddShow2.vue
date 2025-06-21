<template>
    <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading">Add Show and Allot Theaters</h3> <button @click="closeShow" class="btn btn-dark new">Close</button></span>
            <form>
                <input type="text" v-model="newShowName" placeholder="Show Name" required>
      <input  v-model="newShowdescription" placeholder="Show Description">
      <form>
        <input type="file" @change="onImageChange" accept="image/*">
      </form>
      <label class="new4">Show Rating</label>
      <input type="range" v-model="newShowRating" placeholder="Rating" min="0" max="10" required>
      <h5>{{ this.newShowRating }}</h5>
      <input type="text" v-model="newShowTags" placeholder="Tags" required>
      <input type="text" v-model="newShowGenre" placeholder="Genre" required>
      <label class="new4" for="Start-date">Date</label>
      <input type="date" name="Start-date" v-model="newShowStart_date" placeholder="Starts ON">
      <label class="new4" for="Start-time">Starts at</label>
      <input type="time" name="Start-time" v-model="newShowTime" placeholder="Time" required>
      <label  class="new4" for="Show-time">Show Duration</label>
      <div>
      <input type="number" v-model="newShowdurationhours" min="0" max="23" @input="updateDuration" /> hours
    </div>
    <div>
      <input type="number" v-model="newShowdurationmins" min="0" max="59" @input="updateDuration" /> minutes
    </div>
    <div class="create-heading">Allot Theaters</div>
    <div v-for="theater in theaters" :key="theater.id">
    {{ theater.name }} in {{ theater.city }}
    <button v-if="!selectedTheaters.includes(theater.id)" @click="addtheater(theater.id)" class="btn btn-dark new">Allot +</button>
    <button v-if="selectedTheaters.includes(theater.id)" @click="removetheater(theater.id)" class="btn btn-dark new">Remove</button>
        <input 
        type="number"
        v-model="ticketPrices[theater.id]"
        v-if="selectedTheaters.includes(theater.id)"
        min="0"
        step="0.01"
        required
        placeholder="Price for Theater"
        />

    </div>
    <div v-for="error in errors" :key="error.length">
        <p class="error">{{ error }}</p>
    </div>


            </form>
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="createShow" class="create-button">Create + </button>
        </div>
        
    </div>

</template>
<script>
import axios  from "axios";
export default{
    name:'AddShow_new',
    data(){
        return {
        newShowName:'',
        newShowdescription:'',
        newShowStart_date:null,
        newShowRating:'',
        newShowTags:[],
        newShowTime:'',
        newShowdurationhours:'',
        newShowdurationmins:'',
        newShowGenre:'',
        selectedFile:null,
        message_f:'',
        message_s:'',
        errors:[],
        selectedTheaters:[],
        ticketPriceslist:[],
        ticketPrices:{},
        theaters:[]
        }
    },
    watch:{
        selectedTheaters(newSelectedTheaters){
            console.log(newSelectedTheaters)
        }

    },
    created() {
        this.fetchTheaters();

    },
    components:{
    },
    methods:{
        createShow(){
            if(!this.newShowName){
                this.errors.push("Enter Show Name")
            }
            if(!this.newShowRating){
                this.errors.push("Enter the Show rating")
            }
            if(!this.newShowStart_date){
                this.errors.push("Enter the Show Start Date")
            }
            if(!this.newShowTime){
                this.errors.push("Enter the Show start time")
            }
            if(!this.newShowTicketPrice){
                this.errors.push("Enter the Show's Ticket Price")
            }
            const time_total= this.newShowdurationhours*60 + this.newShowdurationmins;
            if(this.errors.length != 0){
                console.log(this.errors)
                this.errors=[]
                this.message_f="Enter the required Details"
                return;
            }
            const allocatedTheaters = this.selectedTheaters.map((theaterid) => ({
                theater_id :theaterid,
                price: parseFloat(this.ticketPrices[theaterid])
            }));
            const token=localStorage.getItem('token')
            const formdata = new FormData();
            formdata.append('name',this.newShowName);
            formdata.append('description',this.newShowdescription)
            formdata.append('rating', this.newShowRating);
            formdata.append('tags', this.newShowTags);
            formdata.append('Date_s', this.newShowStart_date);
            formdata.append('genre',this.newShowGenre)
            formdata.append('interval',time_total);
            formdata.append('time',this.newShowTime);

            formdata.append('ticketPricelist',JSON.stringify(this.ticketPrices))
            console.log(this.ticketPrices)
            //add the theater and price list 
            formdata.append('theaters',this.selectedTheaters)
            formdata.append('prices',JSON.stringify(this.allocatedTheaters))
            formdata.append('image', this.selectedFile);
            console.log(formdata)
            console.log(allocatedTheaters);
            console.log(JSON.stringify(allocatedTheaters))
            
            axios.post(`http://localhost:5000/api/shows/create`,formdata,{
  headers: {
    'Content-Type': 'multipart/form-data',
    'Authorization': token
  },
}).then(response => {
      this.message_s=response.data.message;
      setTimeout(() => {
    console.log("Emitting close form!");
    this.closeShow();
  }, 500);

        }).catch(error => {
            this.error=error.message;
        })

        },
        closeShow(){
            this.$router.go(-1); 
        },
        onImageChange(event){
            this.selectedFile=event.target.files[0];
        }
        ,
        fetchTheaters(){
            fetch('http://127.0.0.1:5000/api/theaters',{
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
                this.theaters=data
            })
            .catch(error => {
                console.error('Error fetching Theaters',error);
            })
        },
        addtheater(theater_id)
        {
            this.selectedTheaters.push(theater_id)
        },
        removetheater(theater_id){
            const index = this.selectedTheaters.indexOf(theater_id)
            if(index !== -1){
                this.selectedTheaters.splice(index,1);
            }

        }
       
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
  .new4{
    text-justify: left;
    justify-content: left;
  }
</style>