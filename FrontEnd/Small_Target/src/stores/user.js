import { defineStore } from 'pinia'
import { authAPI } from '@/utils/requests.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '', // 持久化存储Token
    userInfo: {}
  }),
  actions: {
    // 设置token
    setToken(token) {
      this.token = token
      localStorage.setItem('token', token)
    },
    // 登录接口
    async login(formData) {
      const res = await authAPI.login(formData)
      // this.setToken(res.data.data.token)
      return res
    },
    // 退出登录
    logout() {
      this.token = ''
      this.userInfo = {}
      localStorage.removeItem('token')
    },
    // 获取用户信息
    async getUserInfo() {
      const res = await authAPI.getUserInfo()
      this.userInfo = res.data.data
      return res
    }
  }
})
