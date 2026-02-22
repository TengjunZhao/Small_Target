import axios from 'axios'
import { useUserStore } from '@/stores/user.js'
import { ElMessage } from 'element-plus' // 如需UI组件提示

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000', // 后端接口地址（在.env文件配置）
  timeout: 5000
})

// 请求拦截器：携带Token（排除登录相关请求）
service.interceptors.request.use(
  (config) => {
    // 检查是否为登录相关请求
    const isAuthRequest = config.url.endsWith('/api/login/') ||
                         config.url.includes('/api/register/') ||
                         config.url.includes('/api/token/');

    // 非登录请求才添加token
    if (!isAuthRequest) {
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
    } else {
      console.log('登录相关请求，不添加Authorization头:', config.url)
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

// API 接口模块化封装

// 认证相关API
export const authAPI = {
  // 登录
  login: (data) => service.post('/login/', data),

  // 注册
  register: (data) => service.post('/login/register/', data),

  // 获取用户信息
  getUserInfo: () => service.get('/login/user/info/'),

  // 刷新token
  refreshToken: () => service.post('/token/refresh/')
}

// 项目管理相关API
export const projectAPI = {
  // 项目相关
  getProjects: () => service.get('/projects/projects/'),
  createProject: (data) => service.post('/projects/projects/', data),
  updateProject: (id, data) => service.put(`/projects/projects/${id}/`, data),
  deleteProject: (id) => service.delete(`/projects/projects/${id}/`),

  // 任务相关
  getTasks: (projectId) => service.get(`/projects/projects/${projectId}/`),
  createTask: (data) => service.post('/projects/tasks/', data),
  updateTask: (id, data) => service.put(`/projects/tasks/${id}/`, data),
  deleteTask: (id) => service.delete(`/projects/tasks/${id}/`)
}

// 财务相关API
export const financeAPI = {
  // 账单导入
  importBill: (data) => service.post('/finance/import-bill/', data),

  // 获取导入状态
  getImportStatus: (params) => service.get('/finance/import-status/', { params }),

  // 用户邮箱配置
  getUserEmailConfig: () => service.get('/finance/user-email-config/'),
  setUserEmailConfig: (data) => service.post('/finance/user-email-config/', data),

  // 待确认支出明细
  getPendingExpenses: (params) => service.get('/finance/pending-expense/', { params }),
  confirmExpense: (data) => service.post('/finance/pending-expense/', data),

  // 收支明细查询
  getBill: (params) => service.get('/finance/bill/', { params }),

  // 家庭成员列表
  getFamilyMembers: () => service.get('/finance/family-members/'),
  
  // 收入类型管理
  getIncomeTypes: () => service.get('/finance/income-types/'),
  createIncomeType: (data) => service.post('/finance/income-types/', data),
  
  // 收入管理
  getIncomes: (params) => service.get('/finance/incomes/', { params }),
  createIncome: (data) => service.post('/finance/incomes/', data),
  
  // 财务分析数据
  getAnalysisData: (params) => service.get('/finance/analysis/', { params }),
}

// Kana相关API
export const kanaAPI = {
  getQuestions: () => service.get('/kana/questions/'),
  submitAnswer: (data) => service.post('/kana/submit-answer/', data),
  getProgress: () => service.get('/kana/progress/'),
  resetProgress: () => service.post('/kana/reset-progress/')
}

// 默认导出axios实例
export default service
