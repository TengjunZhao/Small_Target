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
  background-color: #f5f7fa;
}

.kana-link {
  margin-top: 20px;
  padding: 12px 24px;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.kana-link:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}
</style>
