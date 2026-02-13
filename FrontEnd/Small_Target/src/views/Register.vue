<template>
  <div class="register-container">
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
        class="register-btn"
        :disabled="!isFormValid"
      >
        注册
      </button>
    </form>
    <div class="login-link">
      已有账号？<router-link to="/">立即登录</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/user.js'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import request from '@/utils/requests.js'

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
    const res = await request.post('/login/register/', {
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

<style scoped>
.register-container {
  width: 400px;
  margin: 50px auto;
  padding: 30px;
  border: 1px solid #eee;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.register-container h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.form-item {
  margin-bottom: 20px;
}

.form-item label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #555;
}

.form-item input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-item input:focus {
  outline: none;
  border-color: #409eff;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.error-tip {
  color: #f56c6c;
  font-size: 12px;
  margin-top: 4px;
}

.register-btn {
  width: 100%;
  padding: 12px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 500;
  margin-top: 10px;
}

.register-btn:hover:not(:disabled) {
  background: #66b1ff;
}

.register-btn:disabled {
  background: #a0cfff;
  cursor: not-allowed;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}

.login-link a {
  color: #409eff;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}
</style>
