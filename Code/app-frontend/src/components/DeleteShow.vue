<template>
    <div></div>
        <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading"> Delete Show</h3> <button @click="closedelete" class="btn btn-dark new">Close</button></span>
            <h4>Show Details</h4>
            <h5>Name : {{ this.show.name }}</h5>
            <p class="new"> Are You sure You want to delete this show ? </p>
            <input type="checkbox"  class="custom-checkbox" v-model="ischecked" required>
            <label for="custom-checkbox">Check me</label>
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="deleteShow" class="create-button btn btn-dark new">Delete Theater</button>
        </div>
        
    </div>

</template>
<script>
import axios from 'axios';
export default{
    name:'DeleteTheater',
    props:{
        show:{
            type:Object,
            required:true,
        }
    },
    emits: ['closeshowDelete'],
    data(){
        return {
            message_f:'',
            message_s:'',
            deleteshowname:'',
            ischecked:false,
        };
    },
    computed:{
    },
    mounted(){
        this.assign();
    },
    methods:{
        deleteShow(){
            if(!this.ischecked){
                this.message_f="Kindly Confirm and Check the Box "
                return ;
            }
            const token =localStorage.getItem('token')
            axios.post(`http://localhost:5000/api/shows/delete/${this.show.id}`,null,{
  headers: {
    'Authorization': token
  }
}).then(response => {
  this.message_s=response.data.message;
  setTimeout(() => {
         console.log("emitting close form !")
         this.$emit('closeshowDelete');
        }, 500); 
        }).catch(error => {
            this.message_f=error.message;
        })
        }
        ,
        closedelete(){
            this.$emit('closeshowDelete');
        },
        assign(){
            this.deleteshowname=this.show.name
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
.custom-checkbox {

  width: 20px;
  height: 20px;
  border: 2px solid #333;
  background-color: white;
  border-radius: 4px;
  margin-right: 10px;
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
}


.custom-checkbox:checked {
  background-color: red;
  content: '\2713'; 
  font-size: 16px;
  color: white;
  line-height: 20px;
  text-align: center;
}

</style>