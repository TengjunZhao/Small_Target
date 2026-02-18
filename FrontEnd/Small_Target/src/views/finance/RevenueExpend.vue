<template>
  <div class="app-container">
    <!-- 顶部导航栏 - 复用原有样式 -->
    <header class="page-header">
      <div class="header-inner">
        <button class="hamburger-btn" @click="toggleSidebar">
          <span class="hamburger-icon"></span>
        </button>
        <h1 class="page-title">家庭资产负债分析系统 - 收支管理</h1>
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

    <!-- 主体内容 -->
    <main class="main-content" :class="{ 'sidebar-hidden': !sidebarVisible }">
      <!-- 侧边栏 - 复用原有样式，高亮当前菜单 -->
      <aside class="sidebar" :class="{ 'sidebar-show': sidebarVisible }">
        <div class="menu-list">
          <router-link to="/finance-analysis" class="menu-item">
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
          <router-link to="/revenue-expend" class="menu-item active">
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

      <!-- 内容区域 -->
      <section class="content-wrapper">
        <!-- 功能标签页 -->
        <div class="tab-nav">
          <div
            class="tab-item"
            :class="{ active: activeTab === 'expense-import' }"
            @click="activeTab = 'expense-import'"
          >
            支出导入
          </div>
          <div
            class="tab-item"
            :class="{ active: activeTab === 'income-input' }"
            @click="activeTab = 'income-input'"
          >
            收入录入
          </div>
          <div
            class="tab-item"
            :class="{ active: activeTab === 'data-analysis' }"
            @click="activeTab = 'data-analysis'"
          >
            收支分析
          </div>
          <div
            class="tab-item"
            :class="{ active: activeTab === 'expense-detail' }"
            @click="activeTab = 'expense-detail'"
          >
            支出明细
          </div>
        </div>

        <!-- 支出导入面板 -->
        <div class="panel" v-if="activeTab === 'expense-import'">
          <div class="panel-card">
            <div class="panel-title">账单导入</div>
            <div class="import-form">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">支付宝账单密码：</label>
                  <input
                    type="password"
                    class="form-input"
                    v-model="alipayPassword"
                    placeholder="请输入支付宝账单导出密码"
                  >
                </div>
                <div class="form-group">
                  <label class="form-label">微信账单密码：</label>
                  <input
                    type="password"
                    class="form-input"
                    v-model="wechatPassword"
                    placeholder="请输入微信账单导出密码"
                  >
                </div>
                <div class="form-group">
                  <label class="form-label">所属用户：</label>
                  <select class="form-select" v-model="billUser">
                    <option value="user1">户主</option>
                    <option value="user2">配偶</option>
                    <option value="user3">其他成员</option>
                  </select>
                </div>
              </div>
              <div class="form-actions">
                <button class="btn primary-btn" @click="importBill">导入账单</button>
                <button class="btn default-btn" @click="resetImportForm">重置</button>
              </div>
            </div>
          </div>

          <!-- 导入待确认列表 -->
          <div class="panel-card mt-20" v-if="pendingExpenseList.length > 0">
            <div class="panel-title">待确认支出明细</div>
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>时间</th>
                    <th>金额(元)</th>
                    <th>收/支</th>
                    <th>商品</th>
                    <th>交易对方</th>
                    <th>类别</th>
                    <th>项目</th>
                    <th>调整项目</th>
                    <th>备注</th>
                    <th>操作</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in pendingExpenseList" :key="item.id">
                    <td>{{ item.time }}</td>
                    <td class="text-red">-{{ item.amount }}</td>
                    <td>{{ item.in_out }}</td>
                    <td>{{ item.commodity }}</td>
                    <td>{{ item.person }}</td>
                    <td>{{ item.main_category }}</td>
                    <td>{{ item.sub_category }}</td>
                    <td>
                      <select class="form-select small-select" v-model="item.adjusted_sub_category">
                        <option value="">请选择</option>
                        <option
                          v-for="category in budgetCategories"
                          :key="category.id"
                          :value="category.id"
                        >
                          {{ category.sub_category }}
                        </option>
                      </select>
                    </td>
                    <td>
                      <input
                        type="text"
                        class="form-input small-input"
                        v-model="item.belonging"
                        placeholder="请输入备注"
                      >
                    </td>
                    <td>
                      <button class="btn mini-btn primary-btn" @click="confirmExpense(index)">确认</button>
                    </td>
                  </tr>
                  <tr v-if="pendingExpenseList.length === 0">
                    <td colspan="10" class="empty-row">暂无待确认支出记录</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- 分页控件 -->
            <div class="pagination" v-if="pendingTotalCount > 0">
              <button
                class="btn mini-btn default-btn"
                @click="loadPendingExpenses(pendingCurrentPage - 1)"
                :disabled="pendingCurrentPage === 1"
              >
                上一页
              </button>
              <span class="page-info">
                第 {{ pendingCurrentPage }} 页 / 共 {{ pendingTotalPages }} 页 (总计 {{ pendingTotalCount }} 条)
              </span>
              <button
                class="btn mini-btn default-btn"
                @click="loadPendingExpenses(pendingCurrentPage + 1)"
                :disabled="pendingCurrentPage === pendingTotalPages"
              >
                下一页
              </button>
            </div>
          </div>
        </div>

        <!-- 收入录入面板 -->
        <div class="panel" v-if="activeTab === 'income-input'">
          <div class="panel-card">
            <div class="panel-title">收入录入</div>
            <div class="income-form">
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">收入金额：</label>
                  <input
                    type="number"
                    class="form-input"
                    v-model="incomeForm.amount"
                    placeholder="请输入收入金额"
                    min="0"
                    step="0.01"
                  >
                </div>
                <div class="form-group">
                  <label class="form-label">收入类别：</label>
                  <select class="form-select" v-model="incomeForm.category">
                    <option value="salary">工资收入</option>
                    <option value="bonus">奖金补贴</option>
                    <option value="investment">投资收益</option>
                    <option value="part-time">兼职收入</option>
                    <option value="other">其他收入</option>
                  </select>
                </div>
                <div class="form-group">
                  <label class="form-label">收入时间：</label>
                  <input
                    type="date"
                    class="form-input"
                    v-model="incomeForm.time"
                  >
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">所属用户：</label>
                  <select class="form-select" v-model="incomeForm.user">
                    <option value="user1">户主</option>
                    <option value="user2">配偶</option>
                    <option value="user3">其他成员</option>
                  </select>
                </div>
                <div class="form-group full-width">
                  <label class="form-label">收入备注：</label>
                  <input
                    type="text"
                    class="form-input"
                    v-model="incomeForm.remark"
                    placeholder="请输入收入备注（选填）"
                  >
                </div>
              </div>
              <div class="form-actions">
                <button class="btn primary-btn" @click="submitIncome">提交收入</button>
                <button class="btn default-btn" @click="resetIncomeForm">重置</button>
              </div>
            </div>
          </div>

          <!-- 最近收入列表 -->
          <div class="panel-card mt-20">
            <div class="panel-title">最近收入记录</div>
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>时间</th>
                    <th>金额(元)</th>
                    <th>类别</th>
                    <th>所属用户</th>
                    <th>备注</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in recentIncomeList" :key="index">
                    <td>{{ item.time }}</td>
                    <td class="text-green">+{{ item.amount }}</td>
                    <td>{{ getIncomeCategoryText(item.category) }}</td>
                    <td>{{ getUserText(item.user) }}</td>
                    <td>{{ item.remark || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- 收支分析面板 -->
        <div class="panel" v-if="activeTab === 'data-analysis'">
          <!-- 分类汇总卡片 -->
          <div class="card-row">
            <div class="stat-card">
              <div class="card-title">本月总收入</div>
              <div class="card-value text-green">¥ {{ monthTotalIncome }}</div>
              <div class="card-trend">较上月 +5.2%</div>
            </div>
            <div class="stat-card">
              <div class="card-title">本月总支出</div>
              <div class="card-value text-red">¥ {{ monthTotalExpense }}</div>
              <div class="card-trend">较上月 -2.8%</div>
            </div>
            <div class="stat-card">
              <div class="card-title">本月收支结余</div>
              <div class="card-value">¥ {{ monthBalance }}</div>
              <div class="card-trend">目标 +5000元</div>
            </div>
            <div class="stat-card">
              <div class="card-title">支出占收入比</div>
              <div class="card-value">{{ expenseIncomeRatio }}%</div>
              <div class="card-trend">目标 ≤70%</div>
            </div>
          </div>

          <!-- 图表区域：收支趋势+分类占比 -->
          <div class="chart-grid">
            <div class="chart-card">
              <div class="chart-title">近12个月收支趋势</div>
              <div id="incomeExpenseTrendChart" class="chart-container"></div>
            </div>
            <div class="chart-card">
              <div class="chart-title">本月支出分类占比</div>
              <div id="expenseCategoryChart" class="chart-container"></div>
            </div>
          </div>

          <div class="chart-card full-width">
            <div class="chart-title">本月收入分类占比</div>
            <div id="incomeCategoryChart" class="chart-container"></div>
          </div>
        </div>

        <!-- 支出明细面板 -->
        <div class="panel" v-if="activeTab === 'expense-detail'">
          <div class="panel-card">
            <div class="panel-header">
              <div class="panel-title">支出明细查询</div>
              <div class="search-form">
                <div class="form-group inline-group">
                  <label class="form-label">时间范围：</label>
                  <input
                    type="date"
                    class="form-input small-input"
                    v-model="searchForm.startDate"
                    @change="validateDateRange"
                  >
                  <span class="range-separator">至</span>
                  <input
                    type="date"
                    class="form-input small-input"
                    v-model="searchForm.endDate"
                    @change="validateDateRange"
                  >
                </div>
                <div class="form-group inline-group">
                  <label class="form-label">支出分类：</label>
                  <select class="form-select small-select" v-model="searchForm.category">
                    <option value="">全部</option>
                    <option
                      v-for="category in budgetCategories"
                      :key="category.id"
                      :value="category.id"
                    >
                      {{ category.sub_category }}
                    </option>
                  </select>
                </div>
                <div class="form-group inline-group">
                  <label class="form-label">所属用户：</label>
                  <select class="form-select small-select" v-model="searchForm.user">
                    <option value="">全部</option>
                    <option
                      v-for="member in familyMembers"
                      :key="member.user_id"
                      :value="member.username"
                    >
                      {{ member.username }}
                      <span v-if="member.is_admin">(管理员)</span>
                    </option>
                  </select>
                </div>
                <button class="btn mini-btn primary-btn" @click="searchExpense">查询</button>
              </div>
            </div>
          </div>

          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>序号</th>
                  <th>时间</th>
                  <th>金额(元)</th>
                  <th>商户/说明</th>
                  <th>分类</th>
                  <th>所属用户</th>
                  <th>备注</th>
                  <th>归属</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in billList" :key="item.id">
                  <td>{{ index + 1 + (expenseCurrentPage - 1) * expensePageSize }}</td>
                  <td>{{ item.time }}</td>
                  <td class="text-red">-{{ item.amount }}</td>
                  <td>{{ item.merchant || item.commodity }}</td>
                  <td>{{ item.category }}</td>
                  <td>{{ item.user }}</td>
                  <td>{{ item.remark }}</td>
                  <td>{{ item.belonging }}</td>
                </tr>
                <tr v-if="billList.length === 0">
                  <td colspan="8" class="empty-row">暂无支出明细数据</td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- 分页 -->
          <div class="pagination" v-if="expenseTotalCount > 0">
              <button
                class="btn mini-btn default-btn"
                @click="() => searchExpense(expenseCurrentPage - 1)"
                :disabled="expenseCurrentPage === 1"
              >
                上一页
              </button>
              <span class="page-info">
                第 {{ expenseCurrentPage }} 页 / 共 {{ expenseTotalPages }} 页 (总计 {{ expenseTotalCount }} 条)
              </span>
              <button
                class="btn mini-btn default-btn"
                @click="() => searchExpense(expenseCurrentPage + 1)"
                :disabled="expenseCurrentPage === expenseTotalPages"
              >
                下一页
              </button>
            </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import * as echarts from 'echarts';
import { financeAPI } from '@/utils/requests.js';
import { ElMessage } from 'element-plus';

// 基础响应式数据
const selectedFamily = ref('family1');
const selectedUser = ref('user1');
const sidebarVisible = ref(true);
const activeTab = ref('expense-import');

// 预算分类选项（包含ID和名称）
const budgetCategories = ref([]);

// 家庭成员选项（包含ID和用户名）
const familyMembers = ref([]);

// 支出导入相关
const billType = ref('alipay');
const alipayPassword = ref('');
const wechatPassword = ref('');
const billUser = ref('user1');

// 待确认支出明细相关
const pendingExpenseList = ref([]);
const pendingCurrentPage = ref(1);
const pendingPageSize = ref(10);
const pendingTotalPages = ref(0);
const pendingTotalCount = ref(0);

// 收支明细相关
const searchForm = ref({
  startDate: getFirstDayOfMonth(),
  endDate: new Date().toISOString().split('T')[0],
  category: '',
  user: ''
});

// 获取本月第一天
function getFirstDayOfMonth() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  return `${year}-${month}-01`;
}

// 验证日期范围
function validateDateRange() {
  if (searchForm.value.startDate && searchForm.value.endDate) {
    const startDate = new Date(searchForm.value.startDate);
    const endDate = new Date(searchForm.value.endDate);

    if (startDate > endDate) {
      ElMessage.warning('开始日期不能晚于结束日期');
      // 自动调整日期
      searchForm.value.startDate = searchForm.value.endDate;
      return false;
    }
  }
  return true;
}
const billList = ref([]);
const expenseCurrentPage = ref(1);
const expensePageSize = ref(10);
const expenseTotalPages = ref(0);
const expenseTotalCount = ref(0);

// 收入录入相关
const incomeForm = ref({
  amount: '',
  category: 'salary',
  time: new Date().toISOString().split('T')[0],
  user: 'user1',
  remark: ''
});
const recentIncomeList = ref([
  { time: '2024-05-10', amount: 15000.0, category: 'salary', user: 'user1', remark: '5月工资' },
  { time: '2024-05-15', amount: 2000.0, category: 'bonus', user: 'user1', remark: '交通补贴' },
  { time: '2024-05-20', amount: 850.5, category: 'investment', user: 'user2', remark: '理财收益' }
]);

// 收支分析相关
const monthTotalIncome = ref(17850.5);
const monthTotalExpense = ref(8560.2);
const monthBalance = ref(monthTotalIncome.value - monthTotalExpense.value);
const expenseIncomeRatio = ref(Math.round((monthTotalExpense.value / monthTotalIncome.value) * 100));

// 图表实例
let trendChart = null;
let expenseCategoryChart = null;
let incomeCategoryChart = null;

// 侧边栏切换
const toggleSidebar = () => {
  sidebarVisible.value = !sidebarVisible.value;
  setTimeout(resizeCharts, 100);
};

// 窗口大小调整
const handleResize = () => {
  const isMobile = window.innerWidth < 768;
  sidebarVisible.value = !isMobile;
  resizeCharts();
};

// 获取家庭成员列表
const loadFamilyMembers = async () => {
  try {
    const res = await financeAPI.getFamilyMembers();


    if (res.data.code === 200) {
      familyMembers.value = res.data.data;
    } else {
      console.error('API返回错误状态:', res.data);
      ElMessage.error(res.data.msg || '获取家庭成员失败');
    }
  } catch (error) {
    console.error('获取家庭成员网络错误:', error);
    console.error('错误详情:', {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    });
    ElMessage.error(`获取家庭成员失败: ${error.message}`);
  }
};

// 获取待确认支出明细
const loadPendingExpenses = async (page = 1) => {
  try {
    const res = await financeAPI.getPendingExpenses({
      page: page,
      page_size: pendingPageSize.value
    });

    if (res.data.code === 200) {
      pendingExpenseList.value = res.data.data.records;
      pendingCurrentPage.value = res.data.data.page;
      pendingTotalPages.value = res.data.data.total_pages;
      pendingTotalCount.value = res.data.data.total;

      // 设置预算分类选项（后端返回的是budget_categories）
      budgetCategories.value = res.data.data.budget_categories || [];
      // 为每条记录初始化调整项目字段
      pendingExpenseList.value.forEach(item => {
        item.adjusted_sub_category = '';
      });
    } else {
      console.error('API返回错误状态:', res.data);
      ElMessage.error(res.data.msg || '获取待确认支出明细失败');
    }
  } catch (error) {
    console.error('获取待确认支出明细网络错误:', error);
    console.error('错误详情:', {
      message: error.message,
      response: error.response,
      status: error.response?.status,
      data: error.response?.data
    });
    ElMessage.error(`获取待确认支出明细失败: ${error.message}`);
  }
};

// 确认支出记录
const confirmExpense = async (index) => {
  const item = pendingExpenseList.value[index];

  // 验证必填字段
  if (!item.belonging) {
    ElMessage.warning('请输入备注信息');
    return;
  }

  try {
    // 获取选中的预算分类ID对应的子分类名称
    const selectedCategory = budgetCategories.value.find(cat => cat.id === parseInt(item.adjusted_sub_category));
    const adjustedSubCategory = selectedCategory ? selectedCategory.sub_category : '';

    const res = await financeAPI.confirmExpense({
      transaction_id: item.transaction_id,
      category: item.sub_category,
      belonging: item.belonging,
      adjusted_sub_category: adjustedSubCategory
    });

    if (res.data.code === 200) {
      ElMessage.success('支出记录确认成功');
      // 从列表中移除已确认的记录
      pendingExpenseList.value.splice(index, 1);
      pendingTotalCount.value -= 1;
      // 如果当前页没有数据且不是第一页，则返回上一页
      if (pendingExpenseList.value.length === 0 && pendingCurrentPage.value > 1) {
        pendingCurrentPage.value -= 1;
        await loadPendingExpenses(pendingCurrentPage.value);
      }
    } else {
      ElMessage.error(res.data.msg || '确认支出记录失败');
    }
  } catch (error) {
    console.error('确认支出记录错误:', error);
    ElMessage.error('确认支出记录失败，请稍后重试');
  }
};

// 支出导入方法
const handleFileUpload = (e) => {
  // 模拟文件上传处理
  console.log('上传文件：', e.target.files[0]);
};
const importBill = async () => {
  // 验证输入
  if (!alipayPassword.value && !wechatPassword.value) {
    ElMessage.error('请至少输入一个账单密码');
    return;
  }

  try {
    // 调用账单导入API
    const res = await financeAPI.importBill({
      alipay_password: alipayPassword.value,
      wechat_password: wechatPassword.value,
      user: billUser.value
    });

    if (res.data.code === 200) {
      ElMessage.success('账单导入成功');
      // 重新加载待确认列表
      await loadPendingExpenses(1);
    } else {
      ElMessage.error(res.data.msg || '账单导入失败');
    }
  } catch (error) {
    console.error('账单导入错误:', error);
    ElMessage.error('账单导入失败，请稍后重试');
  }
};
const resetImportForm = () => {
  alipayPassword.value = '';
  wechatPassword.value = '';
  billUser.value = 'user1';
};

// 重置支出明细查询表单
const resetSearchForm = () => {
  searchForm.value = {
    startDate: getFirstDayOfMonth(),
    endDate: new Date().toISOString().split('T')[0],
    category: '',
    user: ''
  };
};

// 收入录入方法
const submitIncome = () => {
  if (!incomeForm.value.amount || incomeForm.value.amount <= 0) {
    alert('请输入有效的收入金额');
    return;
  }
  recentIncomeList.value.unshift({
    ...incomeForm.value,
    amount: parseFloat(incomeForm.value.amount)
  });
  resetIncomeForm();
  alert('收入记录提交成功');
};
const resetIncomeForm = () => {
  incomeForm.value = {
    amount: '',
    category: 'salary',
    time: new Date().toISOString().split('T')[0],
    user: 'user1',
    remark: ''
  };
};

// 辅助文本转换
const getIncomeCategoryText = (category) => {
  const map = {
    salary: '工资收入',
    bonus: '奖金补贴',
    investment: '投资收益',
    part_time: '兼职收入',
    other: '其他收入'
  };
  return map[category] || category;
};
const getExpenseCategoryText = (category) => {
  const map = {
    food: '餐饮美食',
    shopping: '购物消费',
    transport: '交通出行',
    housing: '住房缴费',
    entertainment: '休闲娱乐',
    other: '其他支出'
  };
  return map[category] || category;
};
const getUserText = (user) => {
  const map = {
    user1: '户主',
    user2: '配偶',
    user3: '其他成员'
  };
  return map[user] || user;
};

// 支出明细查询
const searchExpense = async (page = 1) => {
  // 先验证日期范围
  if (!validateDateRange()) {
    return;
  }

  try {
    // 获取选中项的ID
    const selectedUser = familyMembers.value.find(member => member.username === searchForm.value.user);
    // searchForm.category现在存储的是ID，直接使用
    const categoryId = searchForm.value.category || '';
    const res = await financeAPI.getBill({
      page: page,
      page_size: expensePageSize.value,
      user_id: selectedUser ? selectedUser.user_id : '',
      category_id: categoryId,
      startDate: searchForm.value.startDate,
      endDate: searchForm.value.endDate
    });

    if (res.data.code === 200) {
      billList.value = res.data.data.records;
      expenseCurrentPage.value = res.data.data.page;
      expenseTotalPages.value = res.data.data.total_pages;
      expenseTotalCount.value = res.data.data.total;

      // 设置预算分类选项
      budgetCategories.value = res.data.data.budget_categories || [];
    } else {
      ElMessage.error(res.data.msg || '获取支出明细失败');
    }
  } catch (error) {
    console.error('获取支出明细错误:', error);
    ElMessage.error('获取支出明细失败，请稍后重试');
  }
};

// 图表初始化
const initCharts = () => {
  // 1. 收支趋势图
  trendChart = echarts.init(document.getElementById('incomeExpenseTrendChart'));
  trendChart.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入', '支出'], top: 0 },
    grid: { left: '10%', right: '5%', bottom: '10%', top: '15%', containLabel: true },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: { type: 'value', unit: '元', min: 0 },
    series: [
      {
        name: '收入',
        type: 'bar',
        data: [16500, 17200, 16800, 17500, 17850.5, 0],
        itemStyle: { color: '#67C23A' },
        barWidth: '40%'
      },
      {
        name: '支出',
        type: 'bar',
        data: [8900, 9200, 8700, 8800, 8560.2, 0],
        itemStyle: { color: '#F56C6C' },
        barWidth: '40%'
      }
    ]
  });

  // 2. 支出分类饼图
  expenseCategoryChart = echarts.init(document.getElementById('expenseCategoryChart'));
  expenseCategoryChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}元 ({d}%)' },
    legend: { orient: 'vertical', right: '10px', top: 'center', textStyle: { fontSize: 12 } },
    series: [{
      name: '支出占比',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['40%', '50%'],
      data: [
        { value: 2560, name: '餐饮美食' },
        { value: 1890, name: '购物消费' },
        { value: 650, name: '交通出行' },
        { value: 2800, name: '住房缴费' },
        { value: 450.2, name: '休闲娱乐' },
        { value: 210, name: '其他支出' }
      ],
      itemStyle: {
        color: function(params) {
          const colorList = ['#F56C6C', '#E6A23C', '#409EFF', '#67C23A', '#909399', '#C0C4CC'];
          return colorList[params.dataIndex];
        }
      }
    }]
  });

  // 3. 收入分类饼图
  incomeCategoryChart = echarts.init(document.getElementById('incomeCategoryChart'));
  incomeCategoryChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c}元 ({d}%)' },
    legend: { orient: 'vertical', right: '10px', top: 'center', textStyle: { fontSize: 12 } },
    series: [{
      name: '收入占比',
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['40%', '50%'],
      data: [
        { value: 15000, name: '工资收入' },
        { value: 2000, name: '奖金补贴' },
        { value: 850.5, name: '投资收益' },
        { value: 0, name: '兼职收入' },
        { value: 0, name: '其他收入' }
      ],
      itemStyle: {
        color: function(params) {
          const colorList = ['#67C23A', '#409EFF', '#E6A23C', '#909399', '#C0C4CC'];
          return colorList[params.dataIndex];
        }
      }
    }]
  });
};

// 图表自适应
const resizeCharts = () => {
  if (trendChart) trendChart.resize();
  if (expenseCategoryChart) expenseCategoryChart.resize();
  if (incomeCategoryChart) incomeCategoryChart.resize();
};

// 监听标签页切换初始化图表
watch(activeTab, (newVal) => {
  if (newVal === 'data-analysis' && !trendChart) {
    setTimeout(initCharts, 100);
  }
});

// 页面加载时获取用户邮箱配置和待确认支出明细
onMounted(async () => {
  try {
    const res = await financeAPI.getUserEmailConfig();
    if (res.data.code === 200) {
      // 可以在这里处理邮箱配置信息
    }

    // 加载家庭成员列表
    await loadFamilyMembers();

    // 加载待确认支出明细
    await loadPendingExpenses(1);

    // 初始化支出明细数据
    await searchExpense(1);
  } catch (error) {
    console.error('初始化失败:', error);
  }

  handleResize();
  window.addEventListener('resize', handleResize);
  // 初始进入分析页时初始化图表
  if (activeTab.value === 'data-analysis') {
    initCharts();
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (trendChart) trendChart.dispose();
  if (expenseCategoryChart) expenseCategoryChart.dispose();
  if (incomeCategoryChart) incomeCategoryChart.dispose();
});
</script>

<style scoped>
/* 复用原有基础样式 */
.app-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  overflow: hidden;
}

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

.main-content {
  display: flex;
  width: 100%;
  height: calc(100vh - 60px);
  overflow: hidden;
  transition: all 0.3s ease;
}

.main-content.sidebar-hidden .content-wrapper {
  width: 100%;
}

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

.content-wrapper {
  flex: 1;
  padding: 20px;
  box-sizing: border-box;
  overflow-y: auto;
  overflow-x: hidden;
  transition: all 0.3s ease;
}

/* 新增样式 */
.tab-nav {
  display: flex;
  gap: 2px;
  background-color: #fff;
  border-radius: 8px 8px 0 0;
  overflow: hidden;
  margin-bottom: 20px;
}

.tab-item {
  flex: 1;
  height: 48px;
  line-height: 48px;
  text-align: center;
  font-size: 14px;
  color: #666;
  cursor: pointer;
  transition: all 0.2s;
}

.tab-item.active {
  color: #409EFF;
  background-color: #e8f4ff;
  font-weight: 600;
}

.tab-item:hover {
  background-color: #f5f7fa;
}

.panel {
  width: 100%;
}

.panel-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.1);
}

.mt-20 {
  margin-top: 20px;
}

.panel-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #f0f0f0;
}

.form-row {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 200px;
}

.form-group.full-width {
  flex: 100%;
  min-width: 100%;
}

.form-label {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.form-input {
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  color: #333;
  transition: border-color 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: #409EFF;
}

.file-input {
  padding: 8px;
  border: 1px dashed #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
}

.primary-btn {
  background-color: #409EFF;
  color: #fff;
}

.primary-btn:hover {
  background-color: #66b1ff;
}

.default-btn {
  background-color: #f5f7fa;
  color: #666;
  border: 1px solid #dcdfe6;
}

.default-btn:hover {
  background-color: #e8f4ff;
  border-color: #c6e2ff;
}

.mini-btn {
  padding: 4px 8px;
  font-size: 12px;
}

.small-input {
  padding: 4px 8px;
  font-size: 12px;
  min-width: 100px;
}

.small-select {
  padding: 4px 8px;
  font-size: 12px;
  min-width: 100px;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 14px;
}

.data-table th {
  background-color: #f5f7fa;
  padding: 12px 10px;
  text-align: left;
  color: #666;
  font-weight: 600;
  border-bottom: 2px solid #f0f0f0;
}

.data-table td {
  padding: 12px 10px;
  border-bottom: 1px solid #f0f0f0;
  color: #333;
}

.data-table tr:hover {
  background-color: #f8f9fa;
}

.text-red {
  color: #F56C6C;
}

.text-green {
  color: #67C23A;
}

.empty-row {
  text-align: center;
  color: #999;
  padding: 40px 0;
}

.search-form {
  display: flex;
  gap: 10px;
  align-items: center;
  flex-wrap: wrap;
}

.inline-group {
  flex-direction: row;
  align-items: center;
  min-width: auto;
}

.range-separator {
  margin: 0 8px;
  color: #999;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
  padding-top: 10px;
  border-top: 1px solid #f0f0f0;
}

.page-info {
  font-size: 14px;
  color: #666;
}

/* 图表样式复用 */
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

.chart-container {
  width: 100%;
  height: 300px;
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
  .hamburger-btn {
    display: block;
  }

  .sidebar {
    transform: translateX(-100%);
    width: 180px;
  }

  .sidebar.sidebar-show {
    transform: translateX(0);
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
    flex-wrap: wrap;
    gap: 10px;
  }

  .page-title {
    font-size: 16px;
    flex: 1;
  }

  .form-row {
    flex-direction: column;
    gap: 15px;
  }

  .search-form {
    flex-direction: column;
    align-items: flex-start;
  }

  .inline-group {
    width: 100%;
    justify-content: flex-start;
  }

  .tab-item {
    height: 40px;
    line-height: 40px;
    font-size: 12px;
  }
}

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
