<template>
  <div class="app-container">
    <!-- 顶部导航栏 - 修复样式，全屏宽度 -->
    <header class="page-header">
      <div class="header-inner">
        <!-- 汉堡按钮 - 移动端显示 -->
        <button class="hamburger-btn" @click="toggleSidebar">
          <span class="hamburger-icon"></span>
        </button>
        <h1 class="page-title">家庭资产负债分析系统</h1>
        <!-- 用户/家庭选择器 - 修复样式 -->
        <div class="user-family-selector">
          <div class="select-group">
            <label>家庭：</label>
            <select class="form-select" v-model="selectedFamily">
              <option value="family1">测试家庭</option>
              <option value="family2">张三家庭</option>
              <option value="family3">李四家庭</option>
            </select>
          </div>
          <div class="select-group">
            <label>用户：</label>
            <select class="form-select" v-model="selectedUser">
              <option value="user1">户主</option>
              <option value="user2">配偶</option>
              <option value="user3">其他成员</option>
            </select>
          </div>
        </div>
      </div>
    </header>

    <!-- 主体内容 - 全屏填充 -->
    <main class="main-content" :class="{ 'sidebar-hidden': !sidebarVisible }">
      <!-- 侧边栏 - 固定宽度，高度全屏 -->
      <aside class="sidebar" :class="{ 'sidebar-show': sidebarVisible }">
        <div class="menu-list">
          <router-link to="/finance-analysis" class="menu-item active">
            <span>财务总览</span>
          </router-link>
          <div class="menu-item">
            <span>资产负债</span>
          </div>
          <div class="submenu-item">
            <span>资产管理</span>
          </div>
          <div class="submenu-item">
            <span>负债管理</span>
          </div>
          <router-link to="/revenue-expend" class="menu-item">
            <span>收支管理</span>
          </router-link>
          <div class="menu-item">
            <span>财务诊断</span>
          </div>
          <div class="menu-item">
            <span>投资监控</span>
          </div>
        </div>
      </aside>

      <!-- 内容区域 - 填充剩余宽度 -->
      <section class="content-wrapper">
        <!-- 核心数据卡片 -->
        <div class="card-row">
          <div class="stat-card">
            <div class="card-title">总资产</div>
            <div class="card-value">¥ 1,258,900.50</div>
            <div class="card-trend">较上月 +2.3%</div>
          </div>
          <div class="stat-card">
            <div class="card-title">总负债</div>
            <div class="card-value">¥ 425,600.00</div>
            <div class="card-trend">较上月 -1.1%</div>
          </div>
          <div class="stat-card">
            <div class="card-title">净资产</div>
            <div class="card-value">¥ 833,300.50</div>
            <div class="card-trend">较上月 +3.5%</div>
          </div>
          <div class="stat-card">
            <div class="card-title">本月储蓄率</div>
            <div class="card-value">28.5%</div>
            <div class="card-trend">目标 20-40%</div>
          </div>
        </div>

        <!-- 预警提示 -->
        <div class="alert-box">
          <span>预警提示：流动性比率为2.5倍（目标3-6倍），建议增加活期存款</span>
        </div>

        <!-- 图表区域1：趋势图+饼图 -->
        <div class="chart-grid">
          <div class="chart-card">
            <div class="chart-title">净资产近12个月趋势</div>
            <div id="assetTrendChart" class="chart-container"></div>
          </div>
          <div class="chart-card">
            <div class="chart-title">资产结构分布</div>
            <div id="assetStructureChart" class="chart-container"></div>
          </div>
        </div>

        <!-- 图表区域2：雷达图 -->
        <div class="chart-card full-width">
          <div class="chart-title">财务健康度指标</div>
          <div id="indicatorRadarChart" class="radar-chart-container"></div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';

// 响应式数据
const selectedFamily = ref('family1');
const selectedUser = ref('user1');
// 侧边栏显示状态
const sidebarVisible = ref(true);

// 监听屏幕尺寸变化，自动调整侧边栏状态
const handleResize = () => {
  const isMobile = window.innerWidth < 768;
  sidebarVisible.value = !isMobile;
  resizeCharts();
};

// 切换侧边栏显示/隐藏
const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value;
  // 延迟执行，确保DOM更新后再调整图表大小
  setTimeout(resizeCharts, 100);
};

// 图表实例
let trendChart = null;
let structureChart = null;
let radarChart = null;

// 初始化图表
const initCharts = () => {
  // 1. 净资产趋势图
  trendChart = echarts.init(document.getElementById('assetTrendChart'));
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '10%', right: '5%', bottom: '10%', top: '10%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['1月', '3月', '5月', '7月', '9月', '11月']
    },
    yAxis: {
      type: 'value',
      unit: '元',
      min: 0,
      max: 1000000,
      interval: 200000
    },
    series: [{
      name: '净资产',
      type: 'line',
      data: [780000, 800000, 820000, 835000, 850000, 833300.50],
      smooth: true,
      itemStyle: { color: '#409EFF' },
      lineWidth: 2
    }]
  });

  // 2. 资产结构饼图（环形图）
  structureChart = echarts.init(document.getElementById('assetStructureChart'));
  structureChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}元 ({d}%)' },
    legend: {
      orient: 'vertical',
      right: '10px',
      top: 'center',
      textStyle: { fontSize: 12 }
    },
    series: [{
      name: '资产占比',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['40%', '50%'],
      data: [
        { value: 350000, name: '投资性资产' },
        { value: 680000, name: '自用性资产' },
        { value: 28900.50, name: '流动性资产' },
        { value: 0, name: '其他资产' }
      ],
      itemStyle: {
        color: function(params) {
          const colorList = ['#409EFF', '#67C23A', '#909399', '#E6A23C'];
          return colorList[params.dataIndex];
        }
      },
      label: { show: false }
    }]
  });

  // 3. 财务指标雷达图
  radarChart = echarts.init(document.getElementById('indicatorRadarChart'));
  radarChart.setOption({
    tooltip: { trigger: 'item' },
    radar: {
      indicator: [
        { name: '资产负债率(%)', max: 50 },
        { name: '流动性比率(倍)', max: 6 },
        { name: '储蓄率(%)', max: 40 },
        { name: '固定支出占比(%)', max: 60 },
        { name: '被动收入占比(%)', max: 100 },
        { name: '资产增值效率(%)', max: 100 }
      ],
      radius: '70%',
      center: ['50%', '50%']
    },
    series: [{
      name: '当前值/目标值',
      type: 'radar',
      data: [
        {
          value: [33.8, 2.5, 28.5, 55, 15, 27.8],
          name: '当前值'
        },
        {
          value: [50, 4.5, 30, 60, 30, 30],
          name: '目标值'
        }
      ]
    }]
  });
};

// 窗口自适应
const resizeCharts = () => {
  if (trendChart) trendChart.resize();
  if (structureChart) structureChart.resize();
  if (radarChart) radarChart.resize();
};

// 生命周期
onMounted(() => {
  // 初始化时判断屏幕尺寸
  handleResize();
  initCharts();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (trendChart) trendChart.dispose();
  if (structureChart) structureChart.dispose();
  if (radarChart) radarChart.dispose();
});
</script>

<style scoped>
/* 全局容器 - 全屏填充 */
.app-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  overflow: hidden;
}

/* 顶部导航 - 修复样式，全屏宽度 */
.page-header {
  width: 100%;
  height: 60px;
  background-color: #fff;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  align-items: center;
  padding: 0 20px;
  box-sizing: border-box;
  position: relative;
}

.header-inner {
  width: 100%;
  max-width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 汉堡按钮样式 */
.hamburger-btn {
  display: none;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 8px;
  margin-right: 10px;
  z-index: 100;
}

.hamburger-icon {
  display: block;
  width: 24px;
  height: 2px;
  background-color: #333;
  position: relative;
  transition: all 0.3s ease;
}

.hamburger-icon::before,
.hamburger-icon::after {
  content: '';
  position: absolute;
  width: 24px;
  height: 2px;
  background-color: #333;
  left: 0;
  transition: all 0.3s ease;
}

.hamburger-icon::before {
  top: -8px;
}

.hamburger-icon::after {
  bottom: -8px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0;
}

/* 用户/家庭选择器 - 修复样式 */
.user-family-selector {
  display: flex;
  gap: 15px;
  align-items: center;
}

.select-group {
  display: flex;
  align-items: center;
  gap: 5px;
}

.select-group label {
  font-size: 14px;
  color: #666;
}

.form-select {
  padding: 5px 10px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
  background-color: #fff;
  cursor: pointer;
}

/* 主体内容 - 全屏填充剩余高度 */
.main-content {
  display: flex;
  width: 100%;
  height: calc(100vh - 60px);
  overflow: hidden;
  transition: all 0.3s ease;
}

/* 侧边栏隐藏时的样式 */
.main-content.sidebar-hidden .content-wrapper {
  width: 100%;
}

/* 侧边栏 - 固定宽度，高度全屏 */
.sidebar {
  width: 200px;
  height: 100%;
  background-color: #fff;
  border-right: 1px solid #e6e6e6;
  padding: 20px 0;
  box-sizing: border-box;
  transition: all 0.3s ease;
  transform: translateX(-100%);
  position: absolute;
  z-index: 99;
  top: 60px;
  left: 0;
  height: calc(100vh - 60px);
}

/* 侧边栏显示样式 */
.sidebar.sidebar-show {
  transform: translateX(0);
  box-shadow: 2px 0 8px rgba(0,0,0,0.1);
}

.menu-list {
  width: 100%;
}

.menu-item {
  height: 40px;
  line-height: 40px;
  padding: 0 20px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.menu-item.active {
  color: #409EFF;
  background-color: #e8f4ff;
  border-left: 3px solid #409EFF;
}

.menu-item:hover {
  color: #409EFF;
}

.submenu-item {
  height: 36px;
  line-height: 36px;
  padding: 0 30px;
  font-size: 13px;
  color: #666;
  cursor: pointer;
}

.submenu-item:hover {
  color: #409EFF;
}

/* 内容区域 - 填充剩余宽度，滚动显示 */
.content-wrapper {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
  transition: all 0.3s ease;
}

/* 数据卡片 - 修复布局 */
.card-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
  text-align: center;
}

.card-title {
  font-size: 14px;
  color: #999;
  margin-bottom: 8px;
}

.card-value {
  font-size: 22px;
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
}

.card-trend {
  font-size: 12px;
  color: #666;
}

/* 预警提示 */
.alert-box {
  background-color: #fdf6ec;
  border: 1px solid #f5dab1;
  border-radius: 4px;
  padding: 12px 15px;
  margin-bottom: 20px;
  color: #E6A23C;
  font-size: 14px;
}

/* 图表区域 - 修复布局 */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.full-width {
  grid-column: 1 / -1;
}

.chart-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  margin-bottom: 10px;
}

.chart-container {
  width: 100%;
  height: 300px;
}

.radar-chart-container {
  width: 100%;
  height: 400px;
}

/* 响应式适配 */
@media (max-width: 1200px) {
  .card-row {
    grid-template-columns: repeat(2, 1fr);
  }
  .chart-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  /* 移动端显示汉堡按钮 */
  .hamburger-btn {
    display: block;
  }

  /* 移动端默认隐藏侧边栏 */
  .sidebar {
    transform: translateX(-100%);
  }

  .sidebar.sidebar-show {
    transform: translateX(0);
  }

  .sidebar {
    width: 180px;
  }

  .card-row {
    grid-template-columns: 1fr;
  }

  .user-family-selector {
    flex-direction: column;
    gap: 5px;
    align-items: flex-end;
  }

  .page-header {
    height: auto;
    padding: 10px 20px;
  }

  .main-content {
    height: calc(100vh - 80px);
  }

  .header-inner {
    justify-content: space-between;
    align-items: center;
  }

  .page-title {
    font-size: 16px;
  }
}

/* 桌面端样式 */
@media (min-width: 769px) {
  .sidebar {
    transform: translateX(0) !important;
    position: static;
    height: 100%;
    box-shadow: none;
  }

  .main-content.sidebar-hidden .sidebar {
    display: block;
  }
}
</style>
