<template>
  <div class="min-h-screen bg-gradient-to-br from-purple-500 to-indigo-700 py-5 px-4">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h1 class="text-white text-4xl md:text-5xl font-bold mb-6 drop-shadow-lg">日语50音练习</h1>
        <div class="flex flex-wrap justify-center gap-4">
          <span class="bg-white bg-opacity-20 text-white px-4 py-2 rounded-full font-semibold backdrop-blur-sm">✅ 正确: {{ correctCount }}</span>
          <span class="bg-white bg-opacity-20 text-white px-4 py-2 rounded-full font-semibold backdrop-blur-sm">❌ 错误: {{ wrongCount }}</span>
        </div>
      </div>
      
      <div class="bg-white rounded-2xl shadow-2xl p-8 mb-8 text-center">
        <div class="text-8xl md:text-9xl font-bold text-gray-800 mb-6">{{ currentKanaDisplay }}</div>
        <div v-if="showHint" class="text-blue-500 text-lg italic p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
          提示: 点击下方选项选择正确的罗马音
        </div>
      </div>
      
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4 mb-8 max-w-2xl mx-auto">
        <button
          v-for="(option, index) in options"
          :key="index"
          class="py-4 px-6 text-xl font-semibold rounded-xl transition-all duration-300 transform hover:scale-105 disabled:transform-none"
          :class="{
            'bg-green-500 hover:bg-green-600 text-white shadow-lg': isAnswered && option === currentKana?.romaji,
            'bg-red-500 hover:bg-red-600 text-white shadow-lg': isAnswered && option === selectedOption && option !== currentKana?.romaji,
            'bg-blue-500 hover:bg-blue-600 text-white shadow-lg': !isAnswered
          }"
          @click="handleAnswerClick(option)"
          :disabled="isAnswered"
        >
          {{ option }}
        </button>
      </div>
      
      <div class="bg-white rounded-2xl shadow-2xl p-6 mb-6">
        <h3 class="text-gray-800 text-2xl font-bold text-center mb-6">🎯 练习统计</h3>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div class="text-center p-4 bg-blue-50 rounded-xl border-2 border-blue-200">
            <div class="text-3xl font-bold text-blue-600">{{ correctCount }}</div>
            <div class="text-gray-600 font-medium">正确数</div>
          </div>
          <div class="text-center p-4 bg-red-50 rounded-xl border-2 border-red-200">
            <div class="text-3xl font-bold text-red-600">{{ wrongCount }}</div>
            <div class="text-gray-600 font-medium">错误数</div>
          </div>
          <div class="text-center p-4 bg-purple-50 rounded-xl border-2 border-purple-200">
            <div class="text-3xl font-bold text-purple-600">{{ totalAttempts }}</div>
            <div class="text-gray-600 font-medium">总练习</div>
          </div>
          <div class="text-center p-4 bg-green-50 rounded-xl border-2 border-green-200">
            <div class="text-3xl font-bold text-green-600">{{ accuracyRate }}%</div>
            <div class="text-gray-600 font-medium">正确率</div>
          </div>
        </div>
        
        <div class="border-t pt-6">
          <h4 class="text-gray-800 text-xl font-bold text-center mb-4">📚 错误记录（高频练习）</h4>
          <div class="max-h-60 overflow-y-auto">
            <div v-if="errorKanaList.length === 0" class="text-center py-6 text-green-600 font-medium">
              🎉 暂无错误记录，继续保持！
            </div>
            <div
              v-for="(kana, index) in errorKanaList"
              :key="index"
              class="flex justify-between items-center p-4 mb-3 bg-red-50 rounded-lg border-l-4 border-red-500"
            >
              <span class="text-lg font-semibold text-gray-800">{{ kana.hira }}/{{ kana.kata }}</span>
              <span class="text-gray-600 italic">({{ kana.romaji }})</span>
              <span class="font-bold text-red-600">❌ {{ kana.errors }}次</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="text-center">
        <button 
          class="px-6 py-3 bg-red-500 hover:bg-red-600 text-white font-semibold rounded-full transition-all duration-300 transform hover:scale-105 shadow-lg"
          @click="resetPractice"
        >
          🔄 重置练习进度
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
const userId = 1; // 简化：使用固定游客账户

const currentKana = ref({ hira: '', kata: '', romaji: '' })
const currentKanaDisplay = ref('')
const options = ref([])
const isAnswered = ref(false)
const selectedOption = ref('')
const correctCount = ref(0)
const wrongCount = ref(0)
const errorKanaList = ref([])
const showHint = ref(true) // 默认显示提示

// 计算属性
const totalAttempts = computed(() => correctCount.value + wrongCount.value)
const accuracyRate = computed(() => {
  if (totalAttempts.value === 0) return 0
  return Math.round((correctCount.value / totalAttempts.value) * 100)
})

const fetchNextKana = async () => {
  try {
    // 获取下一题
    const res = await fetch(`/api/kana/next/?user_id=${userId}`)
    const data = await res.json()
    currentKana.value = { hira: data.hira, kata: data.kata, romaji: data.romaji }
    currentKanaDisplay.value = Math.random() > 0.5 ? data.hira : data.kata
    options.value = data.options || []
    
    // 重置答题状态
    isAnswered.value = false
    selectedOption.value = ''
    
    // 获取最新的错误记录
    await fetchErrorList()
  } catch (e) {
    console.error(e)
  }
}

const logResult = async (correct) => {
  try {
    const response = await fetch('/api/kana/log/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, romaji: currentKana.value.romaji, correct }),
    })
    const result = await response.json()
    console.log('记录结果:', result)
    
    // 如果记录成功，重新获取最新的统计信息（可选）
    // 这里我们先保持本地状态，因为后端返回了progress信息
    if (result.message === '记录成功') {
      // 可以选择更新本地状态为后端返回的值，但通常本地状态更准确
    }
  } catch (e) {
    console.error('记录结果失败:', e)
  }
}

const handleAnswerClick = async (option) => {
  const isCorrect = option === currentKana.value.romaji
  isAnswered.value = true
  selectedOption.value = option
  
  if (isCorrect) {
    correctCount.value++
  } else {
    wrongCount.value++
  }
  
  // 隐藏提示
  showHint.value = false
  
  // 记录结果
  await logResult(isCorrect)
  
  // 延迟获取下一题，让用户看到结果
  setTimeout(() => {
    showHint.value = true // 重新显示提示
    fetchNextKana()
  }, 1500)
}

const fetchErrorList = async () => {
  try {
    const res = await fetch(`/api/kana/errors/?user_id=${userId}&limit=10`)
    const data = await res.json()
    errorKanaList.value = data.error_list || []
  } catch (e) {
    console.error('获取错误列表失败:', e)
    errorKanaList.value = []
  }
}

const resetPractice = async () => {
  correctCount.value = 0
  wrongCount.value = 0
  await fetchNextKana()
}

onMounted(async () => {
  await fetchNextKana()
  // 初始加载错误记录
  await fetchErrorList()
})
</script>
