<template>
  <div class="kana-practice-container">
    <div class="container">
      <h1>日语50音练习</h1>
      <div class="kana-display">{{ currentKanaDisplay }}</div>
      <div class="options">
        <button
          v-for="(option, index) in options"
          :key="index"
          class="option-btn"
          :class="{
            correct: isAnswered && option === currentKana?.romaji,
            wrong: isAnswered && option === selectedOption
          }"
          @click="handleAnswerClick(option)"
          :disabled="isAnswered"
        >
          {{ option }}
        </button>
      </div>
      <div class="stats">
        <h3>练习统计</h3>
        <p>正确数: {{ correctCount }}</p>
        <p>错误数: {{ wrongCount }}</p>
        <div class="error-list">
          <strong>错误记录（高频练习）:</strong>
          <div>
            <div v-if="errorKanaList.length === 0" class="error-item">暂无错误记录</div>
            <div
              v-for="(kana, index) in errorKanaList"
              :key="index"
              class="error-item"
            >
              {{ kana.hira }}/{{ kana.kata }} ({{ kana.romaji }}) - 错误{{ kana.errors }}次
            </div>
          </div>
        </div>
      </div>
      <button class="reset-btn" @click="resetPractice">重置练习进度</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

// 日语50音数据（响应式）
const kanaData = ref([
  { hira: 'あ', kata: 'ア', romaji: 'a', weight: 5, errors: 0 },
  { hira: 'い', kata: 'イ', romaji: 'i', weight: 5, errors: 0 },
  { hira: 'う', kata: 'ウ', romaji: 'u', weight: 5, errors: 0 },
  { hira: 'え', kata: 'エ', romaji: 'e', weight: 5, errors: 0 },
  { hira: 'お', kata: 'オ', romaji: 'o', weight: 5, errors: 0 },
  { hira: 'か', kata: 'カ', romaji: 'ka', weight: 5, errors: 0 },
  { hira: 'き', kata: 'キ', romaji: 'ki', weight: 5, errors: 0 },
  { hira: 'く', kata: 'ク', romaji: 'ku', weight: 5, errors: 0 },
  { hira: 'け', kata: 'ケ', romaji: 'ke', weight: 5, errors: 0 },
  { hira: 'こ', kata: 'コ', romaji: 'ko', weight: 5, errors: 0 },
  { hira: 'さ', kata: 'サ', romaji: 'sa', weight: 5, errors: 0 },
  { hira: 'し', kata: 'シ', romaji: 'shi', weight: 5, errors: 0 },
  { hira: 'す', kata: 'ス', romaji: 'su', weight: 5, errors: 0 },
  { hira: 'せ', kata: 'セ', romaji: 'se', weight: 5, errors: 0 },
  { hira: 'そ', kata: 'ソ', romaji: 'so', weight: 5, errors: 0 },
  { hira: 'た', kata: 'タ', romaji: 'ta', weight: 5, errors: 0 },
  { hira: 'ち', kata: 'チ', romaji: 'chi', weight: 5, errors: 0 },
  { hira: 'つ', kata: 'ツ', romaji: 'tsu', weight: 5, errors: 0 },
  { hira: 'て', kata: 'テ', romaji: 'te', weight: 5, errors: 0 },
  { hira: 'と', kata: 'ト', romaji: 'to', weight: 5, errors: 0 },
  { hira: 'な', kata: 'ナ', romaji: 'na', weight: 5, errors: 0 },
  { hira: 'に', kata: 'ニ', romaji: 'ni', weight: 5, errors: 0 },
  { hira: 'ぬ', kata: 'ヌ', romaji: 'nu', weight: 5, errors: 0 },
  { hira: 'ね', kata: 'ネ', romaji: 'ne', weight: 5, errors: 0 },
  { hira: 'の', kata: 'ノ', romaji: 'no', weight: 5, errors: 0 },
  { hira: 'は', kata: 'ハ', romaji: 'ha', weight: 5, errors: 0 },
  { hira: 'ひ', kata: 'ヒ', romaji: 'hi', weight: 5, errors: 0 },
  { hira: 'ふ', kata: 'フ', romaji: 'fu', weight: 5, errors: 0 },
  { hira: 'へ', kata: 'ヘ', romaji: 'he', weight: 5, errors: 0 },
  { hira: 'ほ', kata: 'ホ', romaji: 'ho', weight: 5, errors: 0 },
  { hira: 'ま', kata: 'マ', romaji: 'ma', weight: 5, errors: 0 },
  { hira: 'み', kata: 'ミ', romaji: 'mi', weight: 5, errors: 0 },
  { hira: 'む', kata: 'ム', romaji: 'mu', weight: 5, errors: 0 },
  { hira: 'め', kata: 'メ', romaji: 'me', weight: 5, errors: 0 },
  { hira: 'も', kata: 'モ', romaji: 'mo', weight: 5, errors: 0 },
  { hira: 'や', kata: 'ヤ', romaji: 'ya', weight: 5, errors: 0 },
  { hira: 'ゆ', kata: 'ユ', romaji: 'yu', weight: 5, errors: 0 },
  { hira: 'よ', kata: 'ヨ', romaji: 'yo', weight: 5, errors: 0 },
  { hira: 'ら', kata: 'ラ', romaji: 'ra', weight: 5, errors: 0 },
  { hira: 'り', kata: 'リ', romaji: 'ri', weight: 5, errors: 0 },
  { hira: 'る', kata: 'ル', romaji: 'ru', weight: 5, errors: 0 },
  { hira: 'れ', kata: 'レ', romaji: 're', weight: 5, errors: 0 },
  { hira: 'ろ', kata: 'ロ', romaji: 'ro', weight: 5, errors: 0 },
  { hira: 'わ', kata: 'ワ', romaji: 'wa', weight: 5, errors: 0 },
  { hira: 'を', kata: 'ヲ', romaji: 'wo', weight: 5, errors: 0 },
  { hira: 'ん', kata: 'ン', romaji: 'n', weight: 5, errors: 0 }
]);

// 响应式状态
const correctCount = ref(0);
const wrongCount = ref(0);
const currentKana = ref(null);
const currentKanaDisplay = ref('');
const options = ref([]);
const isAnswered = ref(false);
const selectedOption = ref('');

// 按权重随机选择假名
const selectRandomKana = () => {
  const totalWeight = kanaData.value.reduce((sum, kana) => sum + kana.weight, 0);
  let randomNum = Math.random() * totalWeight;

  for (const kana of kanaData.value) {
    randomNum -= kana.weight;
    if (randomNum <= 0) return kana;
  }
  return kanaData.value[0];
};

// 生成答题选项
const generateOptions = (correctRomaji) => {
  const wrongOptions = kanaData.value
    .filter(kana => kana.romaji !== correctRomaji)
    .map(kana => kana.romaji);

  const shuffledWrong = [...wrongOptions].sort(() => 0.5 - Math.random());
  const selectedWrong = shuffledWrong.slice(0, 2);

  return [correctRomaji, ...selectedWrong].sort(() => 0.5 - Math.random());
};

// 渲染题目
const renderQuestion = () => {
  isAnswered.value = false;
  selectedOption.value = '';
  currentKana.value = selectRandomKana();

  // 随机显示平假名/片假名
  currentKanaDisplay.value = Math.random() > 0.5
    ? currentKana.value.hira
    : currentKana.value.kata;

  options.value = generateOptions(currentKana.value.romaji);
};

// 处理答题点击
const handleAnswerClick = (option) => {
  isAnswered.value = true;
  selectedOption.value = option;

  if (option === currentKana.value.romaji) {
    // 回答正确
    correctCount.value++;
    currentKana.value.weight = Math.max(1, currentKana.value.weight - 1);
  } else {
    // 回答错误
    wrongCount.value++;
    currentKana.value.weight = Math.min(10, currentKana.value.weight + 2);
    currentKana.value.errors++;
  }

  // 1秒后切换下一题
  setTimeout(renderQuestion, 1000);
};

// 错误列表（计算属性）
const errorKanaList = computed(() => {
  return kanaData.value
    .filter(kana => kana.errors > 0)
    .sort((a, b) => b.errors - a.errors);
});

// 重置练习进度
const resetPractice = () => {
  kanaData.value.forEach(kana => {
    kana.weight = 5;
    kana.errors = 0;
  });
  correctCount.value = 0;
  wrongCount.value = 0;
  renderQuestion();
};

// 初始化
onMounted(() => renderQuestion());
</script>

<style scoped>
.kana-practice-container {
  background-color: #f5f7fa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

.container {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 100%;
  max-width: 600px;
  text-align: center;
}

.kana-display {
  font-size: 8rem;
  margin: 30px 0;
  color: #2c3e50;
  font-weight: bold;
}

.options {
  display: grid;
  grid-template-columns: 1fr;
  gap: 15px;
  margin: 20px 0;
}

.option-btn {
  padding: 15px 20px;
  font-size: 1.2rem;
  border: none;
  border-radius: 8px;
  background-color: #3498db;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-btn:hover {
  background-color: #2980b9;
  transform: translateY(-2px);
}

.option-btn.correct {
  background-color: #2ecc71;
}

.option-btn.wrong {
  background-color: #e74c3c;
}

.stats {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  text-align: left;
}

.stats h3 {
  margin-bottom: 10px;
  color: #34495e;
}

.stats p {
  margin: 5px 0;
  color: #7f8c8d;
}

.error-list {
  margin-top: 10px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 6px;
  max-height: 150px;
  overflow-y: auto;
}

.error-item {
  padding: 5px 0;
  border-bottom: 1px dashed #ddd;
}

.reset-btn {
  margin-top: 20px;
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  background-color: #9b59b6;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.reset-btn:hover {
  background-color: #8e44ad;
}

/* 响应式适配 */
@media (max-width: 500px) {
  .kana-display {
    font-size: 6rem;
  }

  .container {
    padding: 20px;
  }
}
</style>
