import { createRouter, createWebHashHistory } from 'vue-router'
import Movies from '../components/Movies.vue'
import Auth from '../components/Auth.vue'

const routes = [
  {
    path: '/',
    name: 'Movies',
    component: Movies
  },
  {
    path: '/auth',
    name: 'Auth',
    component: Auth
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
