<template>
    <div class="summary-page">
      <h1>Theater Summary Page</h1>
      <div class="theater-list">
        <TheaterReport v-for="(theater, index) in theaters" :key="index" :theater="theater" ></TheaterReport>
      </div>
    </div>
  </template>
  
  <script>
  import TheaterReport from './TheaterReport.vue';
  
  export default {
    name:'SummaryPage',
    components: {
    TheaterReport
},
    data() {
      return {
        theaters:[],
      };
    },
    created(){
        this.fetchTheaters();
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
        },}

  };
  </script>
  
  <style scoped>
  .summary-page{
    background-color: #053544;
    color: azure;

  }
  </style>
  