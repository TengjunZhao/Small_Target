<template>
  <div class="home-container">
    <h1>Vue3 主页面</h1>
    <!-- 50音练习跳转链接 -->
    <router-link to="/kana-practice" class="kana-link">
      进入日语50音练习
    </router-link>
  </div>
</template>

<script setup>
// 主页面逻辑
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

h1 {
  color: white;
  font-size: 3rem;
  margin-bottom: 2rem;
  text-align: center;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.kana-link {
  margin-top: 20px;
  padding: 15px 30px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 50px;
  font-size: 1.2rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
}

.kana-link:hover {
  background-color: #2980b9;
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(52, 152, 219, 0.6);
}

/* 响应式设计 */
@media (max-width: 768px) {
  h1 {
    font-size: 2rem;
  }
  
  .kana-link {
    padding: 12px 24px;
    font-size: 1rem;
  }
}
</style>
