<template>
  <div class="auth-container">
    <h2>用户注册</h2>
    <form @submit.prevent="handleRegister">
      <div class="form-item">
        <label>用户名：</label>
        <input
          v-model="form.username"
          type="text"
          placeholder="请输入用户名"
          required
          minlength="3"
          maxlength="150"
        />
        <div v-if="form.username && form.username.length < 3" class="error-tip">
          用户名至少3个字符
        </div>
      </div>
      <div class="form-item">
        <label>邮箱（可选）：</label>
        <input
          v-model="form.email"
          type="email"
          placeholder="请输入邮箱地址"
        />
      </div>
      <div class="form-item">
        <label>密码：</label>
        <input
          v-model="form.password"
          type="password"
          placeholder="请输入密码"
          required
          minlength="6"
        />
        <div v-if="form.password && form.password.length < 6" class="error-tip">
          密码至少6个字符
        </div>
      </div>
      <div class="form-item">
        <label>确认密码：</label>
        <input
          v-model="form.confirmPassword"
          type="password"
          placeholder="请再次输入密码"
          required
        />
        <div v-if="form.confirmPassword && form.password !== form.confirmPassword" class="error-tip">
          两次输入的密码不一致
        </div>
      </div>
      <button
        type="submit"
        class="auth-btn"
        :disabled="!isFormValid"
      >
        注册
      </button>
    </form>
    <div class="auth-link">
      已有账号？<router-link to="/">立即登录</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authAPI } from '@/utils/requests.js'

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

const userStore = useUserStore()
const router = useRouter()

// 表单验证
const isFormValid = computed(() => {
  return (
    form.value.username &&
    form.value.username.length >= 3 &&
    form.value.password &&
    form.value.password.length >= 6 &&
    form.value.password === form.value.confirmPassword
  )
})

const handleRegister = async () => {
  try {
    // 前端验证
    if (!form.value.username || form.value.username.length < 3) {
      ElMessage.error('用户名至少3个字符')
      return
    }

    if (form.value.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.value.email)) {
      ElMessage.error('请输入正确的邮箱格式')
      return
    }

    if (!form.value.password || form.value.password.length < 6) {
      ElMessage.error('密码至少6个字符')
      return
    }

    if (form.value.password !== form.value.confirmPassword) {
      ElMessage.error('两次输入的密码不一致')
      return
    }

    console.log('开始注册...')

    // 调用注册接口
    const res = await authAPI.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password
    })

    console.log('注册响应:', res)

    if (res.data.code === 200) {
      ElMessage.success('注册成功')

      // 自动登录（使用返回的token）
      userStore.setToken(res.data.data.token)
      await userStore.getUserInfo()

      // 跳转到首页
      router.push('/home')
    } else {
      ElMessage.error(res.data.msg || '注册失败')
    }

  } catch (error) {
    console.error('注册错误:', error)
    if (error.response && error.response.data) {
      ElMessage.error(error.response.data.msg || '注册失败')
    } else {
      ElMessage.error('网络错误，请稍后重试')
    }
  }
}
</script>

<!-- 使用全局 main.css 样式，无需额外 scoped 样式 -->
