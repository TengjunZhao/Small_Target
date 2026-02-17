import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'
import Login from '@/views/Login.vue';
import Register from '@/views/Register.vue';
import Home from '@/views/home.vue'; // 主页面
import KanaPractice from '@/views/KanaPractice.vue'; // 50音练习组件
import ProjectManagement from '@/views/ProjectManagement.vue'; // 项目管理组件
import FinanceAnalysis from '@/views/finance/FinanceAnalysis.vue'; // 家庭资产负债分析组件
import RevenueExpend from "@/views/finance/RevenueExpend.vue";

const routes = [
  // 登录页面
  {
    path: '/',
    name: 'login',
    component: Login,
    meta: { requiresAuth: false } // 登录页无需鉴权
  },
  // 注册页面
  {
    path: '/register',
    name: 'register',
    component: Register,
    meta: { requiresAuth: false } // 注册页无需鉴权
  },
  // 以下所有页面均需要登录
  {
    path: '/home',
    name: 'home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/kana-practice',
    name: 'kana-practice',
    component: KanaPractice,
    meta: { requiresAuth: true}
  },
  {
    path: '/projects',
    name: 'projects',
    component: ProjectManagement,
    meta: { requiresAuth: true }
  },
  {
    path: '/finance-analysis',
    name: 'finance-analysis',
    component: FinanceAnalysis,
    meta: { requiresAuth: true }
  },
  {
    path: '/revenue-expend',
    name: 'revenue-expend',
    component: RevenueExpend,
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

  /*console.log('路由守卫触发:', {
    to: to.path,
    from: from.path,
    token: userStore.token ? 'exists' : 'null',
    requiresAuth: to.meta.requiresAuth
  })*/

  // 登录页面逻辑
  if (to.path === '/' || to.name === 'login') {
    console.log('访问登录页面，直接放行')
    next()
    return
  }

  // 需要鉴权的页面
  if (to.meta.requiresAuth) {
    if (userStore.token) {
      console.log('有token，允许访问受保护页面')
      next()
    } else {
      console.log('无token，重定向到登录页')
      next({ path: '/', query: { redirect: to.fullPath } })
    }
  } else {
    // 无需鉴权的页面
    console.log('无需鉴权的页面，直接放行')
    next()
  }
})
export default router
