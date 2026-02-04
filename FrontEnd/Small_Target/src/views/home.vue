<template>
  <div class="min-h-screen flex flex-col items-center justify-center bg-gradient-to-br from-purple-500 to-indigo-700 p-5">
    <h1 class="text-white text-5xl md:text-6xl font-bold mb-8 text-center drop-shadow-lg">
      Vue3 主页面
    </h1>
    <!-- 50音练习跳转链接 -->
    <router-link 
      to="/kana-practice" 
      class="mt-5 px-8 py-4 bg-blue-500 hover:bg-blue-600 text-white text-xl font-semibold rounded-full transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl"
    >
      进入日语50音练习
    </router-link>
  </div>
</template>

<script setup>
// 主页面逻辑
</script>
