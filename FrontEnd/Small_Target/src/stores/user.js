import { defineStore } from 'pinia'
import request from '@/utils/requests.js'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '', // 持久化存储Token
    userInfo: {}
  }),
  actions: {
    // 登录接口
    async login(formData) {
      // console.log('发送登录请求:', formData)
      const res = await request.post('login/', formData)
      // console.log('登录响应:', res)
      // console.log('响应数据结构:', res.data)
      this.token = res.data.data.token
      // console.log('设置token:', this.token)
      localStorage.setItem('token', this.token) // 存入本地缓存
      // console.log('localStorage中的token:', localStorage.getItem('token'))
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
      const res = await request.get('login/user/info/')
      this.userInfo = res.data.data  // 提取实际的用户数据
      return res
    }
  }
})
