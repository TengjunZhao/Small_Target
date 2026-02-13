<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-4 sm:p-6 md:p-8">
    <!-- 标题区域 -->
    <div class="mb-10 text-center">
      <h1 class="text-white text-4xl sm:text-5xl md:text-6xl font-bold mb-3 drop-shadow-lg">
        小目标管理系统
      </h1>
      <p class="text-purple-100 text-lg opacity-80">
        高效管理你的项目与学习目标
      </p>
    </div>

    <!-- 功能导航卡片 -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 w-full max-w-3xl">
      <!-- 项目管理卡片 -->
      <router-link
        to="/projects"
        class="group bg-white/20 backdrop-blur-md rounded-2xl p-8 hover:bg-white/30 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-2xl border border-white/30"
      >
        <div class="flex flex-col items-center text-center">
          <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <h2 class="text-white text-2xl font-bold mb-2">项目管理</h2>
          <p class="text-white/80 text-sm sm:text-base">管理项目进度、任务分解和甘特图</p>
        </div>
      </router-link>

      <!-- 50音练习卡片 -->
      <router-link
        to="/kana-practice"
        class="group bg-white/20 backdrop-blur-md rounded-2xl p-8 hover:bg-white/30 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-2xl border border-white/30"
      >
        <div class="flex flex-col items-center text-center">
          <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
          </div>
          <h2 class="text-white text-2xl font-bold mb-2">日语50音</h2>
          <p class="text-white/80 text-sm sm:text-base">练习平假名和片假名发音</p>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
// 主页面逻辑
</script>

<!-- 可选：组件内补充样式（如果需要） -->
<style scoped>
/* 这里可以加组件专属样式，优先用Tailwind，特殊需求再写自定义CSS */
</style>
