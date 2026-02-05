import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'; // 主页面
import KanaPractice from '../views/KanaPractice.vue'; // 50音练习组件
import ProjectManagement from '../views/ProjectManagement.vue'; // 项目管理组件

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
  {
    path: '/projects',
    name: 'projects',
    component: ProjectManagement,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
