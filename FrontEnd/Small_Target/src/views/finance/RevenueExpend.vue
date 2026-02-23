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
              </div>
              <div class="form-actions">
                <button
                  class="btn primary-btn"
                  @click="importBill"
                  :disabled="isImporting"
                >
                  {{ isImporting ? '导入中...' : '导入账单' }}
                </button>
                <button class="btn default-btn" @click="resetImportForm">重置</button>
              </div>
            </div>
          </div>

          <!-- 导入进度显示 -->
          <div class="panel-card mt-20" v-if="isImporting || importTaskStatus.task_id">
            <div class="panel-title">导入进度</div>
            <div class="progress-container">
              <!-- 任务基本信息 -->
              <div class="task-info" v-if="importTaskStatus.task_id">
                <div class="info-item">
                  <strong>任务ID：</strong>
                  <span class="task-id">{{ importTaskStatus.task_id.substring(0, 8) }}...</span>
                </div>
                <div class="info-item">
                  <strong>状态：</strong>
                  <span class="status-badge" :class="importTaskStatus.status">
                    {{ getStatusText(importTaskStatus.status) }}
                  </span>
                </div>
              </div>

              <!-- 进度概览 -->
              <div class="progress-overview">
                <div class="progress-main">
                  <div class="progress-text">
                    <span class="progress-percent">{{ importTaskStatus.progress }}%</span>
                    <span class="progress-label">完成度</span>
                  </div>
                  <div class="progress-description">
                    {{ getStatusDescription(importTaskStatus.status, importTaskStatus.message) }}
                  </div>
                </div>
                <div class="progress-stats">
                  <div class="stat-item">
                    <span class="stat-number">{{ importTaskStatus.progress }}</span>
                    <span class="stat-label">进度</span>
                  </div>
                  <div class="stat-item">
                    <span class="stat-number">{{ formatTime(new Date()) }}</span>
                    <span class="stat-label">当前时间</span>
                  </div>
                </div>
              </div>

              <!-- 进度条 -->
              <div class="progress-bar-container">
                <div class="progress-bar">
                  <div
                    class="progress-fill"
                    :style="{
                      width: importTaskStatus.progress + '%',
                      backgroundColor: getProgressColor(importTaskStatus.status, importTaskStatus.progress)
                    }"
                  ></div>
                </div>
                <div class="progress-steps">
                  <div
                    class="step"
                    :class="{ active: importTaskStatus.progress >= 25, completed: importTaskStatus.progress > 25 }"
                  >
                    <div class="step-icon">1</div>
                    <div class="step-label">启动任务</div>
                  </div>
                  <div
                    class="step"
                    :class="{ active: importTaskStatus.progress >= 50, completed: importTaskStatus.progress > 50 }"
                  >
                    <div class="step-icon">2</div>
                    <div class="step-label">处理数据</div>
                  </div>
                  <div
                    class="step"
                    :class="{ active: importTaskStatus.progress >= 75, completed: importTaskStatus.progress > 75 }"
                  >
                    <div class="step-icon">3</div>
                    <div class="step-label">合并记录</div>
                  </div>
                  <div
                    class="step"
                    :class="{ active: importTaskStatus.progress >= 100, completed: importTaskStatus.status === 'completed' }"
                  >
                    <div class="step-icon">✓</div>
                    <div class="step-label">完成导入</div>
                  </div>
                </div>
              </div>

              <!-- 详细信息 -->
              <div class="progress-details" v-if="importTaskStatus.result || importTaskStatus.message">
                <div class="detail-section">
                  <h4>任务详情</h4>
                  <div class="detail-item" v-if="importTaskStatus.message">
                    <strong>当前状态：</strong>
                    <span>{{ importTaskStatus.message }}</span>
                  </div>
                  <div class="detail-item" v-if="importTaskStatus.result && importTaskStatus.result.processed_files !== undefined">
                    <strong>处理文件数：</strong>
                    <span>{{ importTaskStatus.result.processed_files }} 个</span>
                  </div>
                  <div class="detail-item" v-if="importTaskStatus.result && importTaskStatus.result.results">
                    <strong>处理结果：</strong>
                    <ul class="result-list">
                      <li v-for="(result, index) in importTaskStatus.result.results" :key="index">
                        {{ result }}
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <!-- 错误详情显示 -->
              <div class="error-details" v-if="importTaskStatus.status === 'failed' && importTaskStatus.message">
                <div class="error-header">
                  <span class="error-icon">⚠️</span>
                  <strong>错误详情:</strong>
                </div>
                <div class="error-message">
                  {{ importTaskStatus.message }}
                </div>
                <div class="error-timestamp" v-if="importTaskStatus.timestamp">
                  发生时间: {{ formatTime(new Date(importTaskStatus.timestamp)) }}
                </div>
              </div>

              <!-- 操作按钮 -->
              <div class="progress-actions" v-if="importTaskStatus.status === 'completed' || importTaskStatus.status === 'failed'">
                <button
                  class="btn default-btn"
                  @click="stopPolling"
                  v-if="importTaskStatus.status === 'failed'"
                >
                  重新尝试
                </button>
                <button
                  class="btn default-btn"
                  @click="clearTaskStatus"
                >
                  清除状态
                </button>
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
                    <th>支出方式</th>
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
                    <td>{{ item.expend_channel }}</td>
                    <td :style="{color: item.in_out === '支出' ? '#F56C6C' : '#67C23A'}">
                      {{ item.in_out === '支出' ? '-' + item.amount : item.amount }}
                    </td>
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
                  <label class="form-label">税前总额（元）：</label>
                  <input
                    type="number"
                    class="form-input"
                    v-model="incomeForm.amount"
                    placeholder="请输入税前总收入"
                    min="0"
                    step="0.01"
                  >
                </div>
                <div class="form-group">
                  <label class="form-label">五险一金和税（元）：</label>
                  <input
                    type="number"
                    class="form-input"
                    v-model="incomeForm.insurance"
                    placeholder="请输入扣除的五险一金和税"
                    min="0"
                    step="0.01"
                  >
                </div>
                <div class="form-group">
                  <label class="form-label">税前调整（元）：</label>
                  <input
                    type="number"
                    class="form-input"
                    v-model="incomeForm.adjustment"
                    placeholder="请输入税前调整金额"
                    step="0.01"
                  >
                </div>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label class="form-label">税后实到（元）：</label>
                  <input
                    type="number"
                    class="form-input"
                    v-model="incomeForm.income"
                    placeholder="请输入实际到账金额"
                    min="0"
                    step="0.01"
                  >
                </div>
                <div class="form-group">
                  <label class="form-label">收入类型：</label>
                  <select class="form-select" v-model="incomeForm.income_type_id">
                    <option value="">请选择收入类型</option>
                    <option
                      v-for="incomeType in incomeTypes"
                      :key="incomeType.id"
                      :value="incomeType.id"
                    >
                      {{ incomeType.income_maintype }} - {{ incomeType.income_subtype }}
                    </option>
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
                  <select class="form-select small-select" v-model="incomeForm.user_id">
                    <option value="">请选择用户</option>
                    <option
                      v-for="member in familyMembers"
                      :key="member.user_id"
                      :value="member.user_id"
                    >
                      {{ member.username }}
                      <span v-if="member.is_admin">(管理员)</span>
                    </option>
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
                    <th>到账日期</th>
                    <th>税前总额(元)</th>
                    <th>扣除项(元)</th>
                    <th>税后实到(元)</th>
                    <th>收入类型</th>
                    <th>所属用户</th>
                    <th>备注</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(item, index) in recentIncomeList" :key="index">
                    <td>{{ item.payday }}</td>
                    <td class="text-green">{{ item.amount }}</td>
                    <td>{{ item.insurance + item.adjustment }}</td>
                    <td class="text-green">{{ item.income }}</td>
                    <td>{{ item.income_type_maintype }}-{{ item.income_type_subtype }}</td>
                    <td>{{ item.user }}</td>
                    <td>{{ item.remark || '-' }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- 收支分析面板 -->
        <div class="panel" v-if="activeTab === 'data-analysis'">
          <!-- 控制选项 -->
          <div class="panel-card mb-20">
            <div class="panel-title">分析设置</div>
            <div class="analysis-controls">
              <div class="control-group">
                <label class="control-label">分析模式：</label>
                <div class="mode-options">
                  <button
                    class="mode-btn"
                    :class="{ active: analysisMode === 'family' }"
                    @click="analysisMode = 'family'"
                  >
                    家庭模式
                  </button>
                  <button
                    class="mode-btn"
                    :class="{ active: analysisMode === 'personal' }"
                    @click="analysisMode = 'personal'"
                  >
                    个人模式
                  </button>
                </div>
              </div>

              <div class="control-group" v-if="analysisMode === 'personal'">
                <label class="control-label">选择用户：</label>
                <select class="form-select" v-model="analysisUserId">
                  <option value="">请选择用户</option>
                  <option
                    v-for="member in familyMembers"
                    :key="member.user_id"
                    :value="member.user_id"
                  >
                    {{ member.username }}
                    <span v-if="member.is_admin">(管理员)</span>
                  </option>
                </select>
              </div>

              <div class="control-group">
                <label class="control-label">时间范围：</label>
                <div class="date-range">
                  <input
                    type="date"
                    class="form-input small-input"
                    v-model="analysisStartDate"
                  >
                  <span class="range-separator">至</span>
                  <input
                    type="date"
                    class="form-input small-input"
                    v-model="analysisEndDate"
                  >
                </div>
              </div>

              <div class="control-group">
                <button class="btn primary-btn" @click="loadAnalysisData">更新分析</button>
              </div>
            </div>
          </div>

          <!-- 加载状态提示 -->
          <div v-if="isAnalysisLoading" class="loading-overlay">
            <div class="loading-spinner"></div>
            <p>正在加载分析数据...</p>
          </div>

          <!-- 分类汇总卡片 -->
          <div class="card-row">
            <div class="stat-card">
              <div class="card-title">总收入</div>
              <div class="card-value text-green">¥ {{ analysisData.totalIncome.toFixed(2) }}</div>
              <div class="card-trend">选定时间段</div>
            </div>
            <div class="stat-card">
              <div class="card-title">总支出</div>
              <div class="card-value text-red">¥ {{ analysisData.totalExpense.toFixed(2) }}</div>
              <div class="card-trend">选定时间段</div>
            </div>
            <div class="stat-card">
              <div class="card-title">收支结余</div>
              <div class="card-value" :class="analysisData.balance >= 0 ? 'text-green' : 'text-red'">¥ {{ analysisData.balance.toFixed(2) }}</div>
              <div class="card-trend">选定时间段</div>
            </div>
            <div class="stat-card">
              <div class="card-title">支出占收入比</div>
              <div class="card-value">{{ analysisData.incomeRatio.toFixed(1) }}%</div>
              <div class="card-trend">选定时间段</div>
            </div>
          </div>

          <!-- 图表区域：收支趋势+分类占比 -->
          <div class="chart-grid">
            <div class="chart-card">
              <div class="chart-title">收支趋势</div>
              <div id="incomeExpenseTrendChart" class="chart-container"></div>
            </div>
            <div class="chart-card">
              <div class="chart-title">支出分类占比</div>
              <div id="expenseCategoryChart" class="chart-container"></div>
            </div>
          </div>

          <div class="chart-card full-width">
            <div class="chart-title">收入分类占比</div>
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
                <button class="btn mini-btn primary-btn" @click="() => searchExpense(1)">查询</button>
              </div>
            </div>
          </div>
          <div class="panel-card mt-20" v-if="billList.length > 0">
            <div class="panel-title">收支明细</div>
            <div class="table-container">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>序号</th>
                    <th>时间</th>
                    <th>金额(元)</th>
                    <th>收入/支出</th>
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
                    <td :style="{color: item.in_out === '支出' ? '#F56C6C' : '#67C23A'}">{{ item.in_out === '支出' ? '-' + item.amount : item.amount }}</td>
                    <td>{{ item.in_out }}</td>
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
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue';
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
const budgetSubCategories = ref([]);

// 家庭成员选项（包含ID和用户名）
const familyMembers = ref([]);

// 支出导入相关
const billType = ref('alipay');
const alipayPassword = ref('');
const wechatPassword = ref('');
const billUser = ref('user1');

// 导入状态管理
const isImporting = ref(false);
const importTaskStatus = ref({
  task_id: '',
  status: '', // pending, processing, completed, failed
  progress: 0,
  message: '',
  result: null,
  timestamp: null,
  error_type: null
});
const pollInterval = ref(null);

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

// 加载分析数据
const loadAnalysisData = async () => {
  if (isAnalysisLoading.value) return; // 防止重复加载
  try {
    isAnalysisLoading.value = true;
    // 验证必要参数
    if (analysisMode.value === 'personal' && !analysisUserId.value) {
      ElMessage.warning('请选择要分析的用户');
      return;
    }

    if (!analysisStartDate.value || !analysisEndDate.value) {
      ElMessage.warning('请选择完整的时间范围');
      return;
    }

    // 构造请求参数
    const params = {
      start_date: analysisStartDate.value,
      end_date: analysisEndDate.value,
      mode: analysisMode.value
    };

    if (analysisMode.value === 'personal') {
      params.user_id = analysisUserId.value;
    }

    // 调用API获取分析数据
    const res = await financeAPI.getAnalysisData(params);

    if (res.data.code === 200) {
      const data = res.data.data;

      // 更新分析数据
      analysisData.value = {
        totalIncome: data.total_income || 0,
        totalExpense: data.total_expense || 0,
        balance: data.balance || 0,
        incomeRatio: data.income_ratio || 0,
        expenseByCategory: data.expense_by_category || [],
        incomeByCategory: data.income_by_category || [],
        monthlyTrend: data.monthly_trend || []
      };

      // 更新图表
      updateCharts();

      ElMessage.success('数据分析更新成功');
    } else {
      ElMessage.error(res.data.msg || '获取分析数据失败');
    }
  } catch (error) {
    console.error('加载分析数据失败:', error);
    ElMessage.error('加载分析数据失败，请稍后重试');
  } finally {
    isAnalysisLoading.value = false;
  }
};

// 更新图表
const updateCharts = () => {
  // 更新收支趋势图
  if (trendChart) {
    const trendData = analysisData.value.monthlyTrend;
    const months = trendData.map(item => item.month);
    const incomes = trendData.map(item => item.income);
    const expenses = trendData.map(item => item.expense);

    trendChart.setOption({
      xAxis: { data: months },
      series: [
        { data: incomes },
        { data: expenses }
      ]
    });
  }

  // 更新支出分类饼图
  if (expenseCategoryChart) {
    const expenseData = analysisData.value.expenseByCategory.map(item => ({
      value: item.amount,
      name: item.category
    }));

    expenseCategoryChart.setOption({
      series: [createPieSeriesConfig('支出占比', expenseData)]
    });
  }

  // 更新收入分类饼图
  if (incomeCategoryChart) {
    const incomeData = analysisData.value.incomeByCategory.map(item => ({
      value: item.amount,
      name: item.category
    }));

    incomeCategoryChart.setOption({
      series: [createPieSeriesConfig('收入占比', incomeData)]
    });
  }
};

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
  income_type_id: '',
  amount: '',
  insurance: '',
  adjustment: '',
  income: '',
  payday: new Date().toISOString().split('T')[0],
  user_id: '',
  remark: ''
});

// 收入类型选项
const incomeTypes = ref([]);

const recentIncomeList = ref([]);

// 收支分析相关
const monthTotalIncome = ref(0);
const monthTotalExpense = ref(0);
const monthBalance = ref(0);
const expenseIncomeRatio = ref(0);

// 分析面板控制变量
const analysisMode = ref('family'); // 'family' 或 'personal'
const analysisUserId = ref(''); // 个人模式下选择的用户ID
const analysisStartDate = ref(getFirstDayOfMonth()); // 分析开始日期
const analysisEndDate = ref(new Date().toISOString().split('T')[0]); // 分析结束日期

// 分析数据加载状态
const isAnalysisLoading = ref(false);

// 分析数据
const analysisData = ref({
  totalIncome: 0,
  totalExpense: 0,
  balance: 0,
  incomeRatio: 0,
  expenseByCategory: [],
  incomeByCategory: [],
  monthlyTrend: []
});

// 图表实例
let trendChart = null;
let expenseCategoryChart = null;
let incomeCategoryChart = null;

// 颜色生成器 - 自动生成不重复的颜色
const generateColors = (count) => {
  const colors = [];
  const baseColors = [
    '#409EFF', '#67C23A', '#E6A23C', '#F56C6C',
    '#909399', '#C0C4CC', '#8cc5ff', '#a4da89',
    '#eebe77', '#f89898', '#c8c9cc', '#e4e7ed'
  ];

  // 如果需要的颜色数量少于基础颜色数量，直接返回对应数量
  if (count <= baseColors.length) {
    return baseColors.slice(0, count);
  }

  // 如果需要更多颜色，则基于HSL生成
  for (let i = 0; i < count; i++) {
    if (i < baseColors.length) {
      colors.push(baseColors[i]);
    } else {
      // 使用HSL生成新颜色，保持良好的视觉效果
      const hue = (i * 137.508) % 360; // 黄金角度分布
      const saturation = 70 + Math.sin(i) * 10;
      const lightness = 50 + Math.cos(i) * 10;
      colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
    }
  }

  return colors;
};

// 创建带有自动颜色的饼图系列配置
const createPieSeriesConfig = (name, data, colors = null) => {
  const actualColors = colors || generateColors(data.length);

  return {
    name: name,
    type: 'pie',
    radius: ['40%', '70%'],
    center: ['40%', '50%'],
    data: data,
    itemStyle: {
      color: function(params) {
        return actualColors[params.dataIndex % actualColors.length];
      }
    }
  };
};

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

// 获取收入类型列表
const loadIncomeTypes = async () => {
  try {
    const res = await financeAPI.getIncomeTypes();

    if (res.data.code === 200) {
      incomeTypes.value = res.data.data;
    } else {
      console.error('API返回错误状态:', res.data);
      ElMessage.error(res.data.msg || '获取收入类型失败');
    }
  } catch (error) {
    console.error('获取收入类型网络错误:', error);
    ElMessage.error(`获取收入类型失败: ${error.message}`);
  }
};

// 获取最近收入记录
const loadRecentIncomes = async () => {
  try {
    const res = await financeAPI.getIncomes({
      page: 1,
      page_size: 10
    });

    if (res.data.code === 200) {
      recentIncomeList.value = res.data.data.records;
    } else {
      console.error('API返回错误状态:', res.data);
      ElMessage.error(res.data.msg || '获取收入记录失败');
    }
  } catch (error) {
    console.error('获取收入记录网络错误:', error);
    ElMessage.error(`获取收入记录失败: ${error.message}`);
  }
};

// 获取预算分类数据
const loadBudgetCategories = async () => {
  try {
    const res = await financeAPI.getBudgetSubCategory();
    
    if (res.data.code === 200 && res.data.data) {
      budgetCategories.value = res.data.data;
      console.log('预算分类数据加载成功:', budgetCategories.value);
    } else {
      console.warn('未能获取预算分类数据');
      budgetCategories.value = [];
    }
  } catch (error) {
    console.error('加载预算分类数据失败:', error);
    budgetCategories.value = [];
  }
};

// 获取待确认支出明细
const loadPendingExpenses = async (page = 1) => {
  try {
    // 先确保预算分类数据已加载
    if (budgetCategories.value.length === 0) {
      await loadBudgetCategories();
    }
    
    const res = await financeAPI.getPendingExpenses({
      page: page,
      page_size: pendingPageSize.value
    });

    if (res.data.code === 200) {
      pendingExpenseList.value = res.data.data.records;
      pendingCurrentPage.value = res.data.data.page;
      pendingTotalPages.value = res.data.data.total_pages;
      pendingTotalCount.value = res.data.data.total;

      // 为每条记录初始化调整项目字段并自动匹配
      pendingExpenseList.value.forEach(item => {
        item.adjusted_sub_category = ''; // 初始化空值

        // 核心逻辑：根据 item.sub_category 匹配 budgetCategories 中的分类，取其 id 赋值
        if (budgetCategories.value.length > 0 && item.sub_category) {
          const matchedCategory = budgetCategories.value.find(
            cate => cate.sub_category === item.sub_category // 按分类名称精确匹配
          );

          if (matchedCategory) {
            item.adjusted_sub_category = matchedCategory.id; // 赋值正确的 id，控件自动选中
            console.log('自动匹配成功:', item.sub_category, '->', matchedCategory.id);
          } else {
            console.log('未找到匹配的分类:', item.sub_category);
            // 如果没有精确匹配，尝试模糊匹配
            const fuzzyMatch = budgetCategories.value.find(
              cate => cate.sub_category.includes(item.sub_category) || 
                     item.sub_category.includes(cate.sub_category)
            );
            if (fuzzyMatch) {
              item.adjusted_sub_category = fuzzyMatch.id;
              console.log('模糊匹配成功:', item.sub_category, '->', fuzzyMatch.id);
            }
          }
        }
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

// 提交收入
const submitIncome = async () => {
  // 验证必填字段
  if (!incomeForm.value.income_type_id) {
    ElMessage.warning('请选择收入类型');
    return;
  }
  if (!incomeForm.value.amount) {
    ElMessage.warning('请输入税前总额');
    return;
  }
  if (!incomeForm.value.income) {
    ElMessage.warning('请输入税后实到金额');
    return;
  }
  if (!incomeForm.value.payday) {
    ElMessage.warning('请选择到账日期');
    return;
  }

  try {
    const requestData = {
      income_type_id: incomeForm.value.income_type_id,
      amount: parseFloat(incomeForm.value.amount),
      insurance: parseFloat(incomeForm.value.insurance) || 0,
      adjustment: parseFloat(incomeForm.value.adjustment) || 0,
      income: parseFloat(incomeForm.value.income),
      payday: incomeForm.value.payday,
      user_id: incomeForm.value.user_id || null,
      remark: incomeForm.value.remark || ''
    };
    console.log('提交收入数据:', requestData)
    const res = await financeAPI.createIncome(requestData);

    if (res.data.code === 200) {
      ElMessage.success('收入记录提交成功');
      resetIncomeForm();
      // 重新加载最近收入列表
      await loadRecentIncomes();
    } else {
      ElMessage.error(res.data.msg || '提交收入失败');
    }
  } catch (error) {
    console.error('提交收入网络错误:', error);
    ElMessage.error(`提交收入失败: ${error.message}`);
  }
};

// 重置收入表单
const resetIncomeForm = () => {
  incomeForm.value = {
    income_type_id: '',
    amount: '',
    insurance: '',
    adjustment: '',
    income: '',
    payday: new Date().toISOString().split('T')[0],
    user_id: '',
    remark: ''
  };
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


// 开始轮询任务状态
const startPolling = (taskId) => {
  // 清除之前的轮询
  if (pollInterval.value) {
    clearInterval(pollInterval.value);
  }

  // 设置新的轮询
  pollInterval.value = setInterval(async () => {
    try {
      const res = await financeAPI.getImportStatus({
        task_id: taskId
      });

      if (res.data.code === 200) {
        const taskData = res.data.data;
        importTaskStatus.value = {
          task_id: taskData.task_id,
          status: taskData.status,
          progress: taskData.progress,
          message: taskData.message,
          result: taskData.result,
          timestamp: taskData.timestamp || null,
          error_type: taskData.error_type || null
        };
        console.log('任务状态:', importTaskStatus.value)

        // 如果任务完成或失败，停止轮询
        if (taskData.status === 'completed' || taskData.status === 'failed') {
          stopPolling();
          isImporting.value = false;

          if (taskData.status === 'completed') {
            ElMessage.success('账单导入成功');
            // 重新加载待确认列表
            await loadPendingExpenses(1);
          } else {
            ElMessage.error(`导入失败: ${taskData.message}`);
          }
        }
      }
    } catch (error) {
      console.error('轮询任务状态失败:', error);
    }
  }, 1000); // 每秒轮询一次
};

// 停止轮询
const stopPolling = () => {
  if (pollInterval.value) {
    clearInterval(pollInterval.value);
    pollInterval.value = null;
  }
};

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '等待中',
    'processing': '处理中',
    'completed': '已完成',
    'failed': '失败'
  };
  return statusMap[status] || status;
};

// 获取状态描述文本
const getStatusDescription = (status, message = '') => {
  const descMap = {
    'pending': '任务已在队列中等待处理',
    'processing': '正在处理账单数据，请耐心等待',
    'completed': '账单导入成功完成',
    'failed': ''
  };

  let baseDesc = descMap[status] || '';

  // 如果有具体的错误信息，添加到描述中
  if (status === 'failed' && message) {
    console.log('错误信息:', message)
    baseDesc = message;
  }
  else{
    baseDesc = descMap[status] || '';
  }

  return baseDesc;
};

// 获取进度条颜色
const getProgressColor = (status, progress) => {
  if (status === 'failed') return '#ff4d4f';
  if (status === 'completed') return '#52c41a';
  if (status === 'processing') {
    // 根据进度变化颜色
    if (progress < 30) return '#1890ff';
    if (progress < 70) return '#40a9ff';
    return '#73d13d';
  }
  return '#d9d9d9';
};

// 格式化时间显示
const formatTime = (dateString) => {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

const importBill = async () => {
  // 验证输入
  if (!alipayPassword.value && !wechatPassword.value) {
    ElMessage.error('请至少输入一个账单密码');
    return;
  }

  try {
    isImporting.value = true;
    importTaskStatus.value = {
      task_id: '',
      status: 'pending',
      progress: 0,
      message: '正在启动导入任务...',
      result: null
    };

    const selectedUser = familyMembers.value.find(member => member.username === searchForm.value.user);
    // 调用账单导入API
    const res = await financeAPI.importBill({
      alipay_password: alipayPassword.value,
      wechat_password: wechatPassword.value,
      user: selectedUser.user_id,
    });

    if (res.data.code === 200) {
      // 启动轮询
      const taskId = res.data.data.task_id;
      importTaskStatus.value.task_id = taskId;
      importTaskStatus.value.message = '任务已启动，正在处理中...';
      startPolling(taskId);
    } else {
      ElMessage.error(res.data.msg || '账单导入任务启动失败');
      isImporting.value = false;
    }
  } catch (error) {
    console.error('账单导入错误:', error);
    ElMessage.error('账单导入失败，请稍后重试');
    isImporting.value = false;
  }
};
const resetImportForm = () => {
  alipayPassword.value = '';
  wechatPassword.value = '';
  billUser.value = 'user1';
};

// 清除任务状态
const clearTaskStatus = () => {
  importTaskStatus.value = {
    task_id: '',
    status: 'pending',
    progress: 0,
    message: '',
    result: null
  };
  isImporting.value = false;
  stopPolling();
  ElMessage.success('任务状态已清除');
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
      await nextTick();
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
      data: []
    },
    yAxis: { type: 'value', unit: '元', min: 0 },
    series: [
      {
        name: '收入',
        type: 'bar',
        data: [],
        itemStyle: { color: '#67C23A' },
        barWidth: '40%'
      },
      {
        name: '支出',
        type: 'bar',
        data: [],
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
      data: [],
      itemStyle: {
        color: function(params) {
          // 动态生成颜色，基于数据索引
          const dataLength = params.seriesData ? params.seriesData.length : 6;
          const colors = generateColors(dataLength);
          return colors[params.dataIndex % colors.length];
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
      data: [],
      itemStyle: {
        color: function(params) {
          // 动态生成颜色，基于数据索引
          const dataLength = params.seriesData ? params.seriesData.length : 5;
          const colors = generateColors(dataLength);
          return colors[params.dataIndex % colors.length];
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

    // 加载基础数据
    await loadFamilyMembers();
    await loadBudgetCategories(); // 先加载预算分类数据
    await loadPendingExpenses(1);

    // 初始进入分析页时初始化图表
    watch(activeTab, async (newVal) => {
      switch (newVal){
        case 'expense-import':
          await loadPendingExpenses(1);
          break;
        case 'income-input':
          await loadIncomeTypes();
          await loadRecentIncomes();
          break;
        case 'data-analysis':
          // 先清理现有图表
          [trendChart, expenseCategoryChart, incomeCategoryChart].forEach(chart => {
            if (chart) {
              chart.dispose();
            }
          });
          // 等待DOM更新
          await nextTick();
          // 初始化图表
          initCharts();
          // 延迟一小段时间确保图表完全初始化后再加载数据
          setTimeout(async () => {
            await loadAnalysisData();
          }, 100);
          break;
        case 'expense-detail':
          // 初始化支出明细数据
          await searchExpense(1);
          break;
      }
      handleResize();
      window.addEventListener('resize', handleResize);
    }, { immediate: true })
  } catch (error) {
    console.error('初始化失败:', error);
  }
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize);
  if (trendChart) trendChart.dispose();
  if (expenseCategoryChart) expenseCategoryChart.dispose();
  if (incomeCategoryChart) incomeCategoryChart.dispose();
  // 清理轮询
  stopPolling();
});
</script>

<style scoped>
/* 复用原有基础样式 */

/* 加载状态样式 */
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #409EFF;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 15px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-overlay p {
  color: #666;
  font-size: 16px;
  margin: 0;
}
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

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
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

/* 控制商品和交易对方列的最大宽度 */
.data-table td:nth-child(4), /* 商品列 */
.data-table th:nth-child(4) {
  max-width: 150px;
  word-wrap: break-word;
  word-break: break-all;
  white-space: normal;
}

.data-table td:nth-child(5), /* 交易对方列 */
.data-table th:nth-child(5) {
  max-width: 120px;
  word-wrap: break-word;
  word-break: break-all;
  white-space: normal;
}

.data-table tr:hover {
  background-color: #f8f9fa;
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

/* 导入进度样式 */
.progress-container {
  padding: 20px;
}

.progress-info {
  margin-bottom: 15px;
}

.progress-text {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-badge.pending {
  background-color: #e6f7ff;
  color: #1890ff;
  border: 1px solid #91d5ff;
}

.status-badge.processing {
  background-color: #fffbe6;
  color: #faad14;
  border: 1px solid #ffe58f;
}

.status-badge.completed {
  background-color: #f6ffed;
  color: #52c41a;
  border: 1px solid #b7eb8f;
}

.status-badge.failed {
  background-color: #fff2f0;
  color: #ff4d4f;
  border: 1px solid #ffccc7;
}

/* 分析面板控制样式 */
.analysis-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  align-items: flex-end;
}

.control-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 200px;
}

.control-label {
  font-weight: 500;
  color: #333;
  font-size: 14px;
}

.mode-options {
  display: flex;
  gap: 10px;
}

.mode-btn {
  padding: 8px 16px;
  border: 1px solid #d9d9d9;
  background: #fff;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 14px;
}

.mode-btn:hover {
  border-color: #409eff;
  color: #409eff;
}

.mode-btn.active {
  background: #409eff;
  border-color: #409eff;
  color: #fff;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.mb-20 {
  margin-bottom: 20px;
}

/* 新增的进度显示样式 */

/* 任务基本信息 */
.task-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
  border: 1px solid #e9ecef;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.task-id {
  font-family: monospace;
  font-size: 14px;
  color: #666;
  background-color: #e9ecef;
  padding: 2px 8px;
  border-radius: 4px;
}

/* 进度概览 */
.progress-overview {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  padding: 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.progress-main {
  flex: 1;
}

.progress-description {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

.progress-stats {
  display: flex;
  gap: 20px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 12px;
  color: #999;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* 进度条容器 */
.progress-bar-container {
  margin-bottom: 30px;
}

.progress-bar {
  width: 100%;
  height: 12px;
  background-color: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.1);
}

.progress-fill {
  height: 100%;
  border-radius: 6px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.progress-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* 步骤指示器 */
.progress-steps {
  display: flex;
  justify-content: space-between;
  position: relative;
}

.progress-steps::before {
  content: '';
  position: absolute;
  top: 12px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #e9ecef;
  z-index: 1;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  position: relative;
}

.step-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #e9ecef;
  color: #999;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  margin-bottom: 8px;
  transition: all 0.3s ease;
  border: 2px solid #e9ecef;
}

.step.active .step-icon {
  background-color: #1890ff;
  color: white;
  border-color: #1890ff;
  transform: scale(1.1);
}

.step.completed .step-icon {
  background-color: #52c41a;
  color: white;
  border-color: #52c41a;
}

.step-label {
  font-size: 12px;
  color: #999;
  text-align: center;
  transition: color 0.3s ease;
}

.step.active .step-label {
  color: #1890ff;
  font-weight: 500;
}

.step.completed .step-label {
  color: #52c41a;
  font-weight: 500;
}

/* 详细信息 */
.detail-section {
  background-color: #fafafa;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #f0f0f0;
}

.detail-section h4 {
  margin: 0 0 15px 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.result-list {
  margin: 8px 0 0 20px;
  padding: 0;
}

.result-list li {
  color: #666;
  font-size: 13px;
  line-height: 1.6;
  margin-bottom: 5px;
}

/* 操作按钮 */
.progress-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
  margin-top: 20px;
}

.progress-percent {
  font-weight: 600;
  color: #333;
}

.progress-message {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background-color: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 15px;
}

.progress-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-fill.processing {
  background: linear-gradient(90deg, #1890ff, #40a9ff);
}

.progress-fill.completed {
  background: linear-gradient(90deg, #52c41a, #73d13d);
}

.progress-fill.failed {
  background: linear-gradient(90deg, #ff4d4f, #ff7875);
}

.progress-details {
  background-color: #fafafa;
  border-radius: 4px;
  padding: 15px;
  border: 1px solid #f0f0f0;
}

.detail-item {
  margin-bottom: 10px;
}

.detail-item:last-child {
  margin-bottom: 0;
}

.detail-item strong {
  color: #333;
  margin-right: 8px;
}

.detail-item ul {
  margin: 5px 0 0 20px;
  padding: 0;
}

.detail-item li {
  color: #666;
  font-size: 13px;
  line-height: 1.4;
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

  /* 在中等屏幕下调整列宽 */
  .data-table td:nth-child(4),
  .data-table th:nth-child(4) {
    max-width: 120px;
  }

  .data-table td:nth-child(5),
  .data-table th:nth-child(5) {
    max-width: 100px;
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

  /* 在小屏幕上进一步调整列宽 */
  .data-table td:nth-child(4),
  .data-table th:nth-child(4) {
    max-width: 100px;
  }

  .data-table td:nth-child(5),
  .data-table th:nth-child(5) {
    max-width: 80px;
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

/* 错误详情样式 */
.error-details {
  background-color: #fef0f0;
  border: 1px solid #fbc4c4;
  border-radius: 8px;
  padding: 15px;
  margin-top: 15px;
}

.error-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
  color: #f56c6c;
  font-size: 14px;
}

.error-icon {
  font-size: 16px;
}

.error-message {
  color: #606266;
  font-size: 13px;
  line-height: 1.5;
  margin-bottom: 8px;
  word-break: break-all;
}

.error-timestamp {
  color: #909399;
  font-size: 12px;
  text-align: right;
}

</style>
