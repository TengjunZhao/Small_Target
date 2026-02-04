<template>
  <div class="kana-practice-container">
    <div class="container">
      <div class="header">
        <h1>日语50音练习</h1>
        <div class="progress-stats">
          <span class="stat-item">✅ 正确: {{ correctCount }}</span>
          <span class="stat-item">❌ 错误: {{ wrongCount }}</span>
        </div>
      </div>
      
      <div class="kana-display-card card">
        <div class="kana-display">{{ currentKanaDisplay }}</div>
        <div class="hint" v-if="showHint">
          提示: 点击下方选项选择正确的罗马音
        </div>
      </div>
      
      <div class="options-grid">
        <button
          v-for="(option, index) in options"
          :key="index"
          class="option-btn btn"
          :class="{
            'btn-success': isAnswered && option === currentKana?.romaji,
            'btn-danger': isAnswered && option === selectedOption && option !== currentKana?.romaji,
            'btn-primary': !isAnswered
          }"
          @click="handleAnswerClick(option)"
          :disabled="isAnswered"
        >
          {{ option }}
        </button>
      </div>
      
      <div class="stats-card card">
        <h3>🎯 练习统计</h3>
        <div class="stats-grid">
          <div class="stat-box">
            <div class="stat-number">{{ correctCount }}</div>
            <div class="stat-label">正确数</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{{ wrongCount }}</div>
            <div class="stat-label">错误数</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{{ totalAttempts }}</div>
            <div class="stat-label">总练习</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{{ accuracyRate }}%</div>
            <div class="stat-label">正确率</div>
          </div>
        </div>
        
        <div class="error-section">
          <h4>📚 错误记录（高频练习）</h4>
          <div class="error-list">
            <div v-if="errorKanaList.length === 0" class="no-errors">
              🎉 暂无错误记录，继续保持！
            </div>
            <div
              v-for="(kana, index) in errorKanaList"
              :key="index"
              class="error-item"
            >
              <span class="kana-chars">{{ kana.hira }}/{{ kana.kata }}</span>
              <span class="kana-romaji">({{ kana.romaji }})</span>
              <span class="error-count">❌ {{ kana.errors }}次</span>
            </div>
          </div>
        </div>
      </div>
      
      <div class="actions">
        <button class="btn btn-danger" @click="resetPractice">
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
  
  // 隐藏提示，显示答案
  showHint.value = false
  
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

<style scoped>
.kana-practice-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.header h1 {
  color: white;
  font-size: 2.5rem;
  margin-bottom: 15px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.progress-stats {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.stat-item {
  background: rgba(255, 255, 255, 0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 600;
  backdrop-filter: blur(10px);
}

.kana-display-card {
  text-align: center;
  margin-bottom: 30px;
}

.kana-display {
  font-size: 8rem;
  margin-bottom: 15px;
  color: #333;
  font-weight: bold;
}

.hint {
  font-size: 1.1rem;
  color: #3498db;
  margin-top: 15px;
  font-style: italic;
  padding: 10px;
  background: rgba(52, 152, 219, 0.1);
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.option-btn {
  font-size: 1.2rem;
  font-weight: 600;
  padding: 15px;
  min-height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stats-card h3 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 15px;
  margin-bottom: 25px;
}

.stat-box {
  text-align: center;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 2px solid #e9ecef;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #3498db;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  font-weight: 500;
}

.error-section h4 {
  color: #333;
  margin-bottom: 15px;
  text-align: center;
}

.error-list {
  max-height: 200px;
  overflow-y: auto;
}

.no-errors {
  text-align: center;
  padding: 20px;
  color: #27ae60;
  font-weight: 500;
}

.error-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 15px;
  background: #fff5f5;
  border-radius: 8px;
  margin-bottom: 8px;
  border-left: 4px solid #e74c3c;
}

.kana-chars {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
}

.kana-romaji {
  color: #666;
  font-style: italic;
}

.error-count {
  font-weight: 600;
  color: #e74c3c;
}

.actions {
  text-align: center;
  margin-top: 20px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header h1 {
    font-size: 2rem;
  }
  
  .kana-display {
    font-size: 5rem;
  }
  
  .options-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .kana-practice-container {
    padding: 10px 0;
  }
  
  .kana-display {
    font-size: 4rem;
  }
  
  .options-grid {
    grid-template-columns: 1fr;
  }
  
  .progress-stats {
    flex-direction: column;
    gap: 10px;
  }
  
  .stat-box {
    padding: 12px;
  }
}
</style>
