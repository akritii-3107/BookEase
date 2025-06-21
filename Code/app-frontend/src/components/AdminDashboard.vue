<template>
    <div class="my-class">
      <div class="special-section">
        <div class="special-section-content">
          <h2>Welcome, {{ user_name }}</h2>
          <div class="special-links">
            <span>            <button type="button" class="btn btn-dark btn-lg user-nav">
                <router-link to="/summary">Summary</router-link>
            </button>
            <button type="button" class="btn btn-dark btn-lg user-nav"  @click="openTheaterModal" >
              Create Theater 
            </button>
            <button type="button" class="btn btn-dark btn-lg user-nav"  @click="openShowModal" >
              Create Show 
            </button>   </span>
          </div>
        </div>
      </div>
      <div class="container responsive">
        <div class="theaters">
    <div class="theater-creation">
        <div>
          <CreateTheater v-if="showTheaterModal" @closeForm="closeTheater"></CreateTheater>
      </div>
      <div class="theater-list">
        <div v-for="theater in theaters" :key="theater.id" class="theater-card">
            <img v-if="theater.image_path" class="theater-image" :src="getImage(theater.image_path)" alt="theater_image">
          <router-link class="new5" :to="{name:'theater_view',params:{theater_id : theater.id}}" ><h4>{{ theater.name }}</h4></router-link>
          <EditTheater :theater="editedTheater" v-if="showEditTheater && theater.id === selected_id" @closeEdit="closeEdit" class="edit-theater"></EditTheater>
          <DeleteTheater :theater="deleteTheater" v-if="showdeleteTheater && theater.id === selected_id_del" @closeDelete="closeDelete" class="edit-theater"></DeleteTheater>
          <AddShow :theater="addedtheater" v-if="dispAddShow && theater.id === selected_id_show" @closeShow="closeShow" class="edit-theater"></AddShow>
          <div class="theater-actions">
            <button @click="openEditfunc(theater)" class="btn btn-dark new" >Edit</button>
            <button @click="deleteTheaterfunc(theater)" class="btn btn-dark new">Delete</button>
            
            <button @click="addShowfunc(theater)" class="btn btn-dark new">Add Show To Theater</button>
          </div>
          <div class="show-list">
            <h5>Shows:</h5>
            <div class="container text-center">
              <hr>
          <div v-for="show in theater.shows" :key="show.id" class="row container text-center">
                <img class="col-3 theater-image show-img" :src="getImage(show.image_path)">
                <div class="col-6"> <router-link class="new5" :to="{name:'show_view',params:{show_id:show.id}}"><h2>{{ show.name }} </h2></router-link>
                </div> 
                <div class="col-3"><button class="btn btn-dark btn-lg new" @click="showShowEdit(show)">Edit</button>
                  <button class="btn btn-dark btn-lg new" @click="showShowDelete(show)">Delete </button></div>
              
                <hr>
                <div v-if="show_showedit && show.id === selected_id_show_edit" class="row">
                  <EditShow @closeshowEdit="closeshowEdit" class="edit-theater" :show="editedshow"></EditShow>
                  <hr>
                </div>
                
                <div v-if="show_showdelete  && show.id === selected_id_show_del" class="row">
                  <DeleteShow @closeshowDelete="closeshowDelete" class="edit-theater" :show="deletedShow"></DeleteShow>
                  <hr>
                </div>
               
 </div>

</div>
          </div>
      </div>
    </div>
        </div>
      </div>
</div>
    </div>
  </template>
  
  <script>
import CreateTheater from './CreateTheater.vue';
import EditTheater from './EditTheater.vue';
import DeleteTheater from './DeleteTheater.vue';
import AddShow from './AddShow.vue';
import EditShow from './EditShow.vue';
import DeleteShow from './DeleteShow.vue';

  export default {
    data(){
        return {
        user_name:localStorage.getItem('username'),
        showTheaterModal: false,
        showShowModal: false,
        message_f:'',
        theaters:[],
        editedTheater:null,
        showEditTheater:false,
        selected_id:'',
        showdeleteTheater:false,
        selected_id_del:null,
        deleteTheater:null,
        showAct:false,
        addedtheater:null,
        dispAddShow:false,
        selected_id_show:null,
        showActions:false,
        show_showedit:false,
        show_showdelete:false,
        editedshow:null,
        deletedShow:null,
        selected_id_show_edit:null,
        selected_id_show_del:null,
        selected_id_show_new:null
        }

    },
    name:'AdminDashboard',
    components:{
        CreateTheater,
        EditTheater,
        DeleteTheater,
        AddShow,
        EditShow,
        DeleteShow,
    },
    created(){
        this.fetchTheaters();
    },
    computed:{
        shouldShowTheaterModal(){
            return this.showTheaterModal
        }
    },
    methods:{
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
        openTheaterModal(){
            this.showTheaterModal=true;
        },
        closeTheater(){
            this.showTheaterModal=false;
            this.fetchTheaters();

        },
        closeEdit(){
          this.showEditTheater=false;
          this.selected_id=null,
          this.fetchTheaters();
        },
        getImage(imagePath){
            return `http://localhost:5000/api/theater-imgs/${imagePath}`

        },
        openEditfunc(theater){
          this.editedTheater=theater;
          this.showEditTheater=true;
          this.selected_id=theater.id
        },
        deleteTheaterfunc(theater){
          this.deleteTheater=theater;
          this.showdeleteTheater=true;
          this.selected_id_del=theater.id

        },
        closeDelete(){
          this.showdeleteTheater=false;
          this.selected_id_del=null,
          this.fetchTheaters();
        },
        addShowfunc(theater){
          this.addedtheater=theater,
          this.dispAddShow=true;
          this.selected_id_show=theater.id
          
        },
        closeShow(){
          this.dispAddShow=false;
          this.selected_id_show=null;     
        },
        openShowModal(){
          this.$router.push('/addShow')
        },

        showShowEdit(show){
          this.show_showedit=true;
          this.editedshow=show
          this.selected_id_show_edit=show.id

        },
        showShowDelete(show){
          this.show_showdelete=true;
          this.deletedShow=show
          this.selected_id_show_del=show.id

        },
        closeshowEdit(){
          this.show_showedit=false;
          this.editedshow=null
          this.selected_id_show_edit=null

        },
        closeshowDelete(){
          this.show_showdelete=false;
          this.deletedShow=null
          this.selected_id_show_del=null


        }
    }
  };
  </script>
  
  <style>
  .special-section {
    background-image: url('../assets/section-bg.png');
    background-size: cover;
    background-position: center;
    height: 120px;
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

  .new5{
    color: #ffffff;
    text-decoration: none;
  }
  
  
  .special-links a {
    color: white;
    text-decoration: none;
    margin-right: 20px;
  }
  .responsive{
    display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  }
  @media screen and (min-width: 768px) {
  .responsive-section {
    flex-direction: row;
    justify-content: center;
  }
}
.my-class{
    background-color: #173e42;
}

.theater-image {
  max-width: 100%;
}
.edit-theater{
  padding-top: 10px;
  padding-bottom: 10px;
  border-radius: 4px;
  border-color: black;
  border: 5px 5px 5px 5px;
  border-bottom: 5px;
  margin-right: 10px;
  margin-bottom: 10px;


}
.delete-theater{
  padding-top: 10px;
  padding-bottom: 10px;
  border-radius: 4px;
  border-color: black;
  border: 5px 5px 5px 5px;

}

.theater-image img {
  max-width: 100%;
  height: auto;
}
.show-img{
  height: 20vh;
  width: 100vh;
}
  .user-nav{
    padding: auto;
    border: 3px;
    margin: 3px;
  }
  .theater-creation {
  margin-bottom: 20px;
  color: rgb(255, 255, 255);
  display: inline-block;
}

.theater-card {
  border: 1px solid black;
  border-radius: 4px;
  padding: 10px;
  align-items: center;
  justify-content: center;
  


  margin-bottom: 10px;
}
.theater-list{
    padding-bottom: 5px;
    padding-top: 5px;
}

.theater-card h4 {
  margin-bottom: 5px;
  border-bottom: 5px;
  margin-right: 10px;
}

.theater-actions button {
  padding-top: 5px;
  border-bottom: 5px;
  margin-right: 10px;

}

.show-list {
  margin-top: 10px;
}
.new{
    display: inline-block;
    justify-content: right;
    padding-bottom: 5px;
    padding-right: 5px;
    margin-bottom: 2px;
    margin-right: 5px;

  }

  </style>
  

