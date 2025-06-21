<template>
    <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading">Add Theater</h3> <button @click="closeTheater" class="btn btn-dark new">Close</button></span>
            <form>
                <input type="text" v-model="newTheaterName" placeholder="Theater Name" required>
      <input type="text" v-model="newTheaterCaption" placeholder="Caption">
      <form>
        <input type="file" @change="onImageChange" accept="image/*">
      </form>
      
      <input type="number" v-model="newTheaterCapacity" placeholder="Capacity" required>

      <input type="text" v-model="newTheaterCity" placeholder="City" required>
      <input type="text" v-model="newTheaterLatitude" placeholder="Latitude">
      <input type="text" v-model="newTheaterLongitude" placeholder="Longitude">
      <button @click="getLocation" class="btn btn-dark new">Get current Location (Latitude and Longitude)access </button>
      <input type="text" v-model="newTheaterAddress" placeholder="Address" required>


            </form>
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="createTheater" class="create-button">Create + </button>
        </div>
        
    </div>

</template>
<script>
import axios  from "axios";
export default{
    name:'CreateTheater',
    data(){
        return {
        newTheaterName:'',
        newTheaterCaption:'',
        newTheaterCity:'',
        selectedFile:null,
        newTheaterCapacity:'',
        newTheaterAddress:'',
        newTheaterLatitude:'',
        newTheaterLongitude:'',
        message_f:'',
        message_s:'',
        error:'',
        }
    },
    components:{
    },
    methods:{
        createTheater(){
            const token=localStorage.getItem('token')
            const formdata = new FormData();
            formdata.append('name',this.newTheaterName);
            formdata.append('caption',this.newTheaterCaption)
            formdata.append('city', this.newTheaterCity);
            formdata.append('capacity', this.newTheaterCapacity);
             formdata.append('address', this.newTheaterAddress);
            formdata.append('latitude', this.newTheaterLatitude);
            formdata.append('longitude', this.newTheaterLongitude);
            formdata.append('image', this.selectedFile);
            axios.post('http://localhost:5000/api/theaters/create',formdata,{
  headers: {
    'Content-Type': 'multipart/form-data',
    'Authorization': token
  },
}).then( response => {
    this.message_s=response.data.message
    setTimeout(() => {
         console.log("emitting close form !")
          this.$emit('closeForm');
        }, 500); 
}).catch(error => {
            this.error=error.message;
            this.message_f=error.message
        })

        },
        closeTheater(){
            this.$emit('closeForm'); 
        },
        onImageChange(event){
            this.selectedFile=event.target.files[0];
        }
        ,
        getLocation(){
            if(navigator.geolocation){
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        this.newTheaterLatitude=position.coords.latitude;
                        this.newTheaterLongitude=position.coords.longitude;
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
</style>