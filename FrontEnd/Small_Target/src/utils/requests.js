import axios from 'axios'
import { useUserStore } from '@/stores/user.js'
import { ElMessage } from 'element-plus' // 如需UI组件提示

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000', // 后端接口地址（在.env文件配置）
  timeout: 5000
})

// 请求拦截器：携带Token
service.interceptors.request.use(
  (config) => {
    // 从localStorage直接获取token，避免Pinia store在拦截器中的问题
    const token = localStorage.getItem('token')
    // console.log('请求拦截器 - Token:', token ? '存在' : '不存在')
    // console.log('请求URL:', config.baseURL + config.url)
    // console.log('localStorage中的token:', token)
    // console.log('完整config:', JSON.stringify(config, null, 2))

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
      // console.log('已添加Authorization头:', config.headers.Authorization)
    } else {
      console.log('警告：未找到token，无法添加Authorization头')
    }
    return config
  },
  (error) => Promise.reject(error)
)

// 响应拦截器：处理Token失效
service.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token过期/无效，强制退出并跳转登录页
      const userStore = useUserStore()
      userStore.logout()
      // window.location.href = '/login'
      ElMessage.error('登录态失效，请重新登录')
    }
    ElMessage.error(error.message || '请求失败')
    return Promise.reject(error)
  }
)

export default service
