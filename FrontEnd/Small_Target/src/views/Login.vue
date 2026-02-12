<template>
  <div class="login-container">
    <h2>系统登录</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-item">
        <label>账号：</label>
        <input v-model="form.username" type="text" placeholder="请输入账号" required />
      </div>
      <div class="form-item">
        <label>密码：</label>
        <input v-model="form.password" type="password" placeholder="请输入密码" required />
      </div>
      <button type="submit" class="login-btn">登录</button>
    </form>
    <div v-if="route.query.redirect" class="redirect-info">
      登录后将跳转到: {{ route.query.redirect }}
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const form = ref({
  username: '',
  password: ''
})
const userStore = useUserStore()
const router = useRouter()
const route = useRoute()

const handleLogin = async () => {
  try {
    console.log('开始登录...')
    const res = await userStore.login(form.value)
    console.log('登录响应:', res)
    // console.log('当前token:', userStore.token)

    // 确保token已设置后再跳转
    if (userStore.token) {
      // console.log('登录成功获得的token:', userStore.token)
      // console.log('token长度:', userStore.token.length)

      // 测试token有效性
      /*try {
        const testRes = await request.get('/login/user/info/')
        console.log('Token测试成功:', testRes.data)
      } catch (testError) {
        console.error('Token测试失败:', testError)
      }*/

      // 获取用户详细信息
      await userStore.getUserInfo()
      console.log('用户信息获取完成:', userStore.userInfo)

      ElMessage.success('登录成功')
      // 检查是否有重定向参数
      const redirect = route.query.redirect || '/home'
      console.log('准备跳转到:', redirect)
      router.push(redirect)
    } else {
      // console.error('Token未设置，无法跳转')
      ElMessage.error('登录状态异常，请重试')
    }
  } catch (error) {
    console.error('登录错误:', error)
    ElMessage.error('账号或密码错误')
  }
}
</script>

<style scoped>
.login-container {
  width: 400px;
  margin: 100px auto;
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 8px;
}
.form-item {
  margin-bottom: 16px;
}
.form-item input {
  width: 100%;
  padding: 8px;
  margin-top: 4px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.login-btn {
  width: 100%;
  padding: 10px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.redirect-info {
  margin-top: 16px;
  padding: 8px;
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 4px;
  color: #0369a1;
  font-size: 14px;
  text-align: center;
}
</style>
