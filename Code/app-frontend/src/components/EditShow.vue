<template>
    <div></div>
        <div class="create-page">
        
        <div class="create-form">
            <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
            <span><h3 class="create-heading">Edit Show</h3> <button @click="closeshowEdit" class="btn btn-dark new">Close</button></span>
            <form>
                <input type="text" v-model="this.editedShowname" placeholder="Show Name">
      <input type="text" v-model="this.editedShowdescription" placeholder="Show Description">
      <form>
        <input type="file" @change="onImageChange" accept="image/*">
      </form>
            </form>
            <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
            <button @click="editShow" class="create-button btn btn-dark new">Edit Show Details</button>
        </div>
        
    </div>

</template>
<script>
import axios from 'axios';
export default{
    props:{
        show:{
            type:Object,
            required:true,
        }
    },
    emits: ['closeshowEdit'],
    data(){
        return {
            message_f:'',
            message_s:'',
            editedShowname:'',
            editedShowdescription:'',
            selectedFile:null,
        };
    },
    computed:{
    },
    mounted(){
        this.assign();
    },
    methods:{
        editShow(){
            if(this.editedShowcapacity < 0){
                this.message_f='Capacity cannot be negative'
            }
            if(this.message_f){
                this.message_f=''
                return;
            }
            const token =localStorage.getItem('token')
            const fd= new FormData()
            fd.append('name',this.editedShowname);
            fd.append('description',this.editedShowdescription);
            fd.append('image',this.selectedFile);
            axios.post(`http://localhost:5000/api/shows/edit/${this.show.id}`,fd,{
  headers: {
    'Content-Type': 'multipart/form-data',
    'Authorization': token
  },
}).then(response => {
        this.message_s=response.data.message
        setTimeout(() => {
         console.log("emitting close form !")
         this.$emit('closeshowEdit');
        }, 1000); 
            
        }).catch(error => {
            this.error=error.message;
        })

        },
        onImageChange(event){
            this.selectedFile=event.target.files[0];
        }
        ,
        closeshowEdit(){
            this.$emit('closeshowEdit');
        },
        assign(){
            this.editedShowname=this.show.name
            this.editedShowdescription=this.show.description

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