<template>
    <div class="report-format">
      <label>Select Report Format:</label>
      <select v-model="selectedFormat">
        <option value="HTML">HTML</option>
        <option value="PDF">PDF</option>
        <option value="Both">Both</option>
      </select>
      <button @click="changeFormat">Change Format</button>
      <div v-if="message_s"  class="p-3 mb-2 bg-success text-white">{{ message_s}}</div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedFormat: 'HTML',
        message_s:'',
      };
    },
    methods: {
      changeFormat() {
        const token = localStorage.getItem('token'); 
        const requestData = {
          format: this.selectedFormat
        };
  

        axios.post(`http://localhost:5000/api/user/reportformat`, requestData, {
          headers: {
            Authorization: token
          }
        })
        .then(response => {
          console.log('Format changed successfully:', response.data);
          this.message_s=response.data.message
          setTimeout(()=>{
            this.message_s=''
          },2000)
        })
        .catch(error => {
          console.error('Error changing format:', error);
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .report-format {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
  }
  </style>
  