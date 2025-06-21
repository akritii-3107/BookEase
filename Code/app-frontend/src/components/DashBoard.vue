<template>
    <main class="display">
    <div v-if="!userRole"  class="p-3 mb-2 bg-info-subtle text-emphasis-info">Log In to access your DashBoard</div>
    <UserDashboard  v-if="userRole === 'user'">
    </UserDashboard>
    <AdminDashboard  v-if="userRole === 'admin'">
    </AdminDashboard>
    <div v-if="message_f"  class="p-3 mb-2 bg-dark-subtle text-emphasis-dark">{{ message_f }}</div>
</main>
</template>
<script>
import UserDashboard from './UserDashboard.vue';
import AdminDashboard from './AdminDashboard.vue';
export default {
    name:'DashBoard',
    components:{
        UserDashboard,
        AdminDashboard,
    },
    data(){
        return {
            userRole:null,
            message_f:''
        }
    },
    created(){
        this.fetchUserRole();
    },
    methods:{
       fetchUserRole() {
        const token = localStorage.getItem('token');
        this.userrole=localStorage.getItem('userole')
        if(!token){
            return;
        }
        if( token && this.userrole){
            return ;
        }
        fetch('http://localhost:5000/api/user/role',{
            headers:{
                'Authorization':token,
            }
        })
        .then(response => {
            if(response.status === 401){
                throw new Error('Token expired or Invalid , Login Again');
                
            }
            if(!response.ok){
                throw new Error('Error retreiving role');
            }
            return response.json();
        })
        .then(data => {
            this.userRole = data.role;

        })
        .catch((error) => {
            this.message_f=error.message;
            setTimeout(() => {
          localStorage.removeItem('token')
          location.reload();
          window.location.href('/');
        }, 1000);
        })
       } 
    }

}
</script>
<style>
.display{
    top: 60px;
    z-index: 1;
}

</style>