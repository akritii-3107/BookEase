import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UserLogin from '../components/UserLogin.vue'
import UserSignup from '../components/UserSignup.vue'
import Dashboard from '../components/DashBoard.vue'
import LogOut from '../components/LogOut.vue'
import CreateTheater from '../components/CreateTheater'
import AdminLogin from '../components/AdminLogin'
import EditTheater from '../components/EditTheater.vue'
import AddShow_new from '../components/AddShow2.vue'
import BookTickets from '../components/BookTickets.vue'
import UserBookings from '../components/UserBookings.vue'
import UserProfile from '../components/UserProfile.vue'
import theater_view from '../components/TheaterHomeview.vue'
import show_view from '../components/ShowHomeview.vue'
import SummaryPage from '../components/SummaryPage.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/contact',
    name: 'ContactPage',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/ContactView.vue')
  },
  {
    path:'/userlogin',
    name:'userlogin',
    component:UserLogin
  },
  {
    path:'/adminlogin',
    name:'adminlogin',
    component:AdminLogin
  },
  {
    path:'/usersignup',
    name:'userSignup',
    component:UserSignup,
  },
  {
    path:'/dashboard',
    name:'dashboard',
    component:Dashboard,
  },
  {
    path:'/logout',
    name:'logout',
    component:LogOut,
  },
  {
    path:'/createTheater',
    name:'create',
    component:CreateTheater
  },
  {
    path:'/editTheater',
    name:'EditTheater',
    component:EditTheater,
  },
  {
    path:'/addShow',
    name:'AddShow_new',
    component:AddShow_new
  },
  {
    path:'/bookTickets',
    name:'BookTickets',
    component:BookTickets,
  },
  {
    path:'/bookings',
    name:'UserBookings',
    component:UserBookings
  },
  {
    path:'/userprofile',
    name:'UserProfile',
    component:UserProfile
  },
  {
    path:'/theater/:theater_id',
    name:'theater_view',
    component:theater_view,
   props: true,
  },
  {
    path:'/show/:show_id',
    name:'show_view',
    component:show_view,
    props:true,
  },
  {
    path:'/summary',
    name:'summary',
    component:SummaryPage,
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
