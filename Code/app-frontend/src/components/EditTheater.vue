<template>
    <div></div>
        <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading">Edit Theater</h3> <button @click="closeEdit" class="btn btn-dark new">Close</button></span>
            <form>
                <input type="text" v-model="this.editedTheatername" placeholder="Theater Name">
      <input type="text" v-model="this.editedTheatercaption" placeholder="Caption">
      <form>
        <input type="file" @change="onImageChange" accept="image/*">
      </form>
      
      <input type="number" v-model="this.editedTheatercapacity" placeholder="Capacity">

      <input type="text" v-model="localcity" placeholder="City" required :disabled="true">

      <input type="text" v-model="localaddress" placeholder="Address" required :disabled="true">


            </form>
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="editTheater" class="create-button btn btn-dark new">Edit Details</button>
        </div>
        
    </div>

</template>
<script>
import axios from 'axios';
export default{
    props:{
        theater:{
            type:Object,
            required:true,
        }
    },
    emits: ['closeEdit'],
    data(){
        return {
            message_f:'',
            message_s:'',
            editedTheatername:'',
            editedTheatercaption:'',
            editedTheatercapacity:'',
            selectedFile:null,
        };
    },
    computed:{
        localcity:{
            get(){
                return this.theater.city
            }
        },
        localaddress:{
            get(){
                return this.theater.address
            }
        },
        localid:{
            get(){
                return this.theater.id
            }
        }
    },
    mounted(){
        this.assign();
    },
    methods:{
        editTheater(){
            if(this.editedTheatercapacity < 0){
                this.message_f='Capacity cannot be negative'
            }
            if(this.message_f){
                this.message_f=''
                return;
            }
            const token =localStorage.getItem('token')
            const fd= new FormData()
            fd.append('name',this.editedTheatername);
            fd.append('caption',this.editedTheatercaption);
            fd.append('capacity',this.editedTheatercapacity);
            fd.append('image',this.selectedFile);
            axios.post(`http://localhost:5000/api/theaters/edit/${this.theater.id}`,fd,{
  headers: {
    'Content-Type': 'multipart/form-data',
    'Authorization': token
  },
}).then(response => {
    this.message_s=response.data.message
            console.log(this.message_s)
            setTimeout(() => {
         console.log("emitting close form !")
         this.$emit('closeEdit');
        }, 500); 
        }).catch(error => {
            this.error=error.message;
            this.message_f=error.message
        })

        },
        getImage(imagePath){
            return `http://localhost:5000/api/theater-imgs/${imagePath}`
        },
        onImageChange(event){
            this.selectedFile=event.target.files[0];
        }
        ,
        closeEdit(){
            this.$emit('closeEdit');
        },
        assign(){
            this.editedTheatername=this.theater.name
            this.editedTheatercaption=this.theater.caption
            this.editedTheatercapacity=this.theater.capacity

        }
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

  }
.edit-theater{
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