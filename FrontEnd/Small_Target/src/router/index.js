import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'; // 主页面
import KanaPractice from '../views/KanaPractice.vue'; // 50音练习组件

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home,
  },
  {
    path: '/kana-practice',
    name: 'kana-practice',
    component: KanaPractice,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
