<template>
    <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading">Add Show</h3> <button @click="closeShow" class="btn btn-dark new">Close</button></span>
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
      <input type="" v-model="newShowTicketPrice" placeholder="Ticket Price" required>
      <label class="new4" for="Start-time">Starts at</label>
      <input type="time" name="Start-time" v-model="newShowTime" placeholder="Time" required>
      <label  class="new4" for="Show-time">Show Duration</label>
      <div>
      <input type="number" v-model="newShowdurationhours" min="0" max="23" @input="updateDuration" /> hours
    </div>
    <div>
      <input type="number" v-model="newShowdurationmins" min="0" max="59" @input="updateDuration" /> minutes
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
    name:'CreateTheater',
    props:{
        theater:{
            type:Object,
            required:true,
        }
    },
    emits:['closeShow'],
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
        newShowTicketPrice:'',
        newShowGenre:'',
        selectedFile:null,
        message_f:'',
        message_s:'',
        errors:[],
        }
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
            if(!this.newShowTicketPrice){
                this.errors.push('Enter the Ticket Price')
            }
            if(!this.newShowStart_date){
                this.errors.push("Enter the Show Start Date")
            }
            if(!this.newShowTime){
                this.errors.push("Enter the Show start time")
            }
            const time_total= this.newShowdurationhours*60 + this.newShowdurationmins;
            if(this.errors.length != 0){
                this.errors=[]
                this.message_f="Enter the required Details"
                return;
            }
            const token=localStorage.getItem('token')
            const formdata = new FormData();
            formdata.append('name',this.newShowName);
            formdata.append('description',this.newShowdescription)
            formdata.append('rating', this.newShowRating);
            formdata.append('tags', this.newShowTags);
            formdata.append('ticket_price', this.newShowTicketPrice);
            formdata.append('Date_s', this.newShowStart_date);
            formdata.append('genre',this.newShowGenre)
            formdata.append('interval',time_total);
            formdata.append('time',this.newShowTime)
            formdata.append('image', this.selectedFile);
            axios.post(`http://localhost:5000/api/shows/create/${this.theater.id}`,formdata,{
  headers: {
    'Content-Type': 'multipart/form-data',
    'Authorization': token
  },
}).then(response => {
          if(!response.ok){
            if(response.status === 401 ){
              return response.json().then(data => {
                this.message_f=data.message;
                throw new Error(data.message);
              });
            }
            if(response.status === 409){
                return response.json().then(data => {
                this.message_f=data.message;
                throw new Error(data.message);
              }); 
            }
            if(response.status === 201){
              this.$emit('closeShow')
            }
          }
        }).then(data => {
            this.message_s=data.message
            console.log(this.message_s)
            setTimeout(() => {
         console.log("emitting close form !")
          this.$emit('closeShow');
        }, 500); 
        }).catch(error => {
            this.error=error.message;
        })

        },
        closeShow(){
            this.$emit('closeShow'); 
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
  .new4{
    text-justify: left;
    justify-content: left;
  }
</style>