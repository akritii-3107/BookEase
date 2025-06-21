<template>
    <div class="theater">
      <h3 class="theater-title">Theater: {{ theater.name }}</h3>
      <h5 class="theater-city">City : {{ theater.city }}</h5>
      <button @click="exportCSV" class="export-button">Export CSV</button>
      <div v-if="showProgressBar" class="progress-container">
        <progress :value="progress" max="100" class="progress-bar"></progress>
        <p class="progress-text">Generating report... {{ progress }}%</p>
        <div class="download-link">
      <a v-if="this.csvDownloadLink" :href="this.csvDownloadLink" download class="csv-download-link">Download CSV</a>
    </div>
      </div>
      <p v-if="message_s" class="p-3 mb-2 bg-success text-white">{{ message_s }}</p>
      <p v-if="message_f" class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</p>
      <div v-if="taskstatus === 'Success'">
    <button @click="downloadFile"  class="download-button">Download File</button>
  </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    name:'TheaterReport',
    props: {
      theater: {
        type: Object,
        required: true
      },
    },
    data() {
      return {
        showProgressBar: false,
        progress: 0,
        message_s: '',
        token:localStorage.getItem('token'),
        csvDownloadLink:null,
        taskstatus:'',
        taskID:'',
        filename:null,
        message_f:''
      };
    },
    methods: {
      async exportCSV() {
        try{
            this.progress = 0;
        this.message_s = '';
        this.taskstatus='running'
        this.showProgressBar = true;
        const token=localStorage.getItem('token')
  
        const response = await axios.post(`http://localhost:5000/api/export_csv/${this.theater.id}`,null,{
            headers:{
                'Authorization':token,
            }
        })
        if(response.data.success){
            this.taskID=response.data.id
            this.message_s=response.data.message
            await this.CheckProgress(this.taskID);
        }
        else{
            console.log('Failed to create CSV File and Export')
            this.message_f=response.data.message
        }

        }
        catch (error){
            console.error(error)
        }

      },
      async CheckProgress(task_id) {
        try{
        const response = await axios.get(`http://localhost:5000/api/get_progress/${task_id}`,{
            headers:{
                'Authorization':this.token,
            },
        })
        const taskstatus=response.data.status;
        if(taskstatus=== 'SUCCESS'){
            this.taskstatus='Success';
            this.progress=100
            this.message_s=response.data.message
            this.filename=response.data.csv_filename
        }
        else if (taskstatus === 'PENDING' || taskstatus === 'RUNNING'){
            await new Promise(resolve => setTimeout(resolve,1000));
            await this.CheckProgress(task_id)
            this.progress=response.status.progress
        }
        else{
            this.message_f="Task Failed with unknown status "
        }

        }
        catch (error){
            console.error(error)
            this.message_f=error.message
        }

      },
      async downloadFile(){
        try {
            const response = await axios.get(`http://localhost:5000/api/get_report_download/${this.filename}`,{
                headers:{
                    'Authorization':this.token
                },
                responseType:'blob'
            });
            const fileData=new Blob([response.data]);
            const fileUrl=URL.createObjectURL(fileData);
            const link = document.createElement('a')
            link.href=fileUrl
            link.download=`Theater_report_${this.theater.name}.csv`;
            link.click();
            URL.revokeObjectURL(fileUrl)
            this.message_f=''
            this.message_s=''
        }
        catch(error){
            this.message_f=('Error in Downloading File.')
            console.error(error)
        }
      }
    }
  };
  </script>
  
  <style scoped>

.theater {
  background-color: #caeded;
  padding: 20px;
  border: 1px solid #053544;
  border-radius: 10px;
  margin: 10px;
}

.theater-title {
  color: #053544;
  font-size: 20px;
  margin-bottom: 5px;
}

.theater-city {
  color: #0e9a99;
  font-size: 16px;
  margin-bottom: 10px;
}

.export-button {
  background-color: #0e9a99;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.progress-container {
  margin-top: 20px;
}

.progress-bar {
  width: 100%;
}

.progress-text {
  margin-top: 5px;
  color: #053544;
}

.csv-download-link {
  color: #053544;
  text-decoration: none;
  margin-top: 5px;
  display: block;
}

.success-message {
  color: #0e9a99;
  margin-top: 10px;
}

.failure-message {
  color: red;
  margin-top: 10px;
}

.download-button-container {
  margin-top: 20px;
}

.download-button {
  background-color: #053544;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

  </style>
  