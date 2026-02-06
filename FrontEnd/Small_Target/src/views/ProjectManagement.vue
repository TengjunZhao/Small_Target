<template>
  <div class="project-management-container">
    <!-- 头部导航 -->
    <el-page-header @back="goBack" title="返回主页">
      <template #content>
        <span class="text-large font-600 mr-3"> 项目管理系统 </span>
      </template>
    </el-page-header>

    <div class="main-content">
      <!-- 项目列表区域 -->
      <div class="project-list-section">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>项目列表</span>
              <el-button type="primary" @click="showCreateDialog = true">
                新建项目
              </el-button>
              <el-button type="success" @click="loadDemoData">
                加载演示数据
              </el-button>
            </div>
          </template>

          <el-table
            :data="projects"
            style="width: 100%"
            @row-click="selectProject"
            :row-class-name="tableRowClassName"
            highlight-current-row
          >
            <el-table-column prop="name" label="项目名称" width="200" />
            <el-table-column prop="description" label="描述" />
            <el-table-column prop="start_date" label="开始日期" width="120" />
            <el-table-column prop="end_date" label="结束日期" width="120" />
            <el-table-column label="状态" width="100">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'info'">
                  {{ scope.row.is_active ? '进行中' : '已结束' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" @click.stop="editProject(scope.row)">编辑</el-button>
                <el-button size="small" type="danger" @click.stop="deleteProject(scope.row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </div>

      <!-- 项目详情区域 - 新增选项卡切换 -->
      <div v-if="selectedProject" class="project-detail-section">
        <el-card class="box-card">
          <template #header>
            <span>项目详情：{{ selectedProject.name }}</span>
          </template>

          <!-- 核心：选项卡组件 -->
          <el-tabs v-model="activeTab" class="w-full">
            <!-- 甘特图选项卡 -->
            <el-tab-pane label="甘特图" name="gantt">
              <div class="w-full h-[600px] p-4 bg-white rounded-lg shadow-md">
                <div ref="ganttRef" class="w-full h-full"></div>
                <div class="mt-4 flex gap-2">
                  <el-button @click="changeView('Day')" class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 transition">
                    日视图
                  </el-button>
                  <el-button @click="changeView('Month')" class="px-4 py-2 bg-gray-200 rounded-md hover:bg-gray-300 transition">
                    月视图
                  </el-button>
                </div>
              </div>
            </el-tab-pane>

            <!-- 任务分解树选项卡 -->
            <el-tab-pane label="任务分解树" name="taskTree">
              <div class="w-full h-[600px] p-4 bg-white rounded-lg shadow-md overflow-auto">
                <!-- 任务树形组件 -->
                <el-tree
                  :data="taskTreeData"
                  :props="treeProps"
                  node-key="id"
                  default-expand-all
                  class="w-full h-full"
                  :expand-on-click-node="false"
                >
                  <!-- 自定义树形节点内容 -->
                  <template #default="{ node, data }">
                    <div class="flex items-center justify-between w-full">
                      <span class="flex items-center">
                        <el-tag v-if="data.progress === 100" type="success" size="small" class="mr-2">已完成</el-tag>
                        <el-tag v-else-if="data.progress > 0" type="warning" size="small" class="mr-2">进行中</el-tag>
                        <el-tag v-else type="info" size="small" class="mr-2">未开始</el-tag>
                        {{ node.label }}
                      </span>
                      <span class="text-sm text-gray-500">进度：{{ data.progress }}%</span>
                    </div>
                  </template>
                </el-tree>
              </div>
            </el-tab-pane>
          </el-tabs>

          <!-- 返回按钮 -->
          <div class="mt-4 flex justify-end">
            <el-button type="primary" @click="handleBack">返回项目列表</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 创建/编辑项目对话框 -->
    <el-dialog v-model="showCreateDialog" :title="editingProject ? '编辑项目' : '新建项目'" width="500px">
      <el-form :model="projectForm" :rules="projectRules" ref="projectFormRef" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="projectForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="projectForm.start_date" type="date" placeholder="选择开始日期" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="projectForm.end_date" type="date" placeholder="选择结束日期" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="saveProject">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import axios from 'axios'
import Gantt from 'frappe-gantt'
import '../assets/frappe-gantt.css'

// 状态管理
const projects = ref([])
const selectedProject = ref(null)
const showCreateDialog = ref(false)
const editingProject = ref(null)
// 新增：选项卡激活状态（默认显示甘特图）
const activeTab = ref('gantt')

// 表单相关
const projectForm = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: ''
})

const projectRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
}

// 甘特图核心配置
const ganttRef = ref(null)
let ganttInstance = null

// 模拟甘特图数据
const ganttData = [
  {
    id: 'task1',
    name: '项目启动',
    start: '2026-02-01',
    end: '2026-02-05',
    progress: 100,
    custom_class: 'bg-green-500'
  },
  {
    id: 'task2',
    name: '需求开发',
    start: '2026-02-06',
    end: '2026-02-20',
    progress: 60
  },
  {
    id: 'task3',
    name: '测试上线',
    start: '2026-02-21',
    end: '2026-03-01',
    progress: 0
  }
]

// 新增：任务分解树数据（和甘特图数据联动）
const taskTreeData = ref([
  {
    id: 'task1',
    label: '项目启动',
    progress: 100,
    children: [
      { id: 'task1-1', label: '需求调研', progress: 100 },
      { id: 'task1-2', label: '立项评审', progress: 100 }
    ]
  },
  {
    id: 'task2',
    label: '需求开发',
    progress: 60,
    children: [
      { id: 'task2-1', label: '接口开发', progress: 80 },
      { id: 'task2-2', label: '页面开发', progress: 50 },
      { id: 'task2-3', label: '逻辑开发', progress: 40 }
    ]
  },
  {
    id: 'task3',
    label: '测试上线',
    progress: 0,
    children: [
      { id: 'task3-1', label: '功能测试', progress: 0 },
      { id: 'task3-2', label: '压力测试', progress: 0 },
      { id: 'task3-3', label: '生产部署', progress: 0 }
    ]
  }
])

// 新增：树形组件配置
const treeProps = ref({
  label: 'label',
  children: 'children'
})

// API基础URL
const API_BASE = '/api'

// 生命周期钩子
onMounted(() => {
  loadProjects()
})

// 方法定义
const goBack = () => {
  window.history.back()
}

// 新增：返回项目列表（重置所有状态）
const handleBack = () => {
  selectedProject.value = null
  activeTab.value = 'gantt' // 重置选项卡
  // 销毁甘特图实例
  if (ganttInstance) {
    try {
      ganttInstance.destroy()
    } catch (e) {
      if (ganttRef.value) ganttRef.value.innerHTML = ''
    }
    ganttInstance = null
  }
}

const loadProjects = async () => {
  try {
    const response = await axios.get(`${API_BASE}/projects/projects/`)
    projects.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    ElMessage.error('加载项目列表失败')
    console.error(error)
    projects.value = []
  }
}

const selectProject = async (project) => {
  selectedProject.value = project
  activeTab.value = 'gantt' // 选中项目默认显示甘特图

  await nextTick()

  // 销毁旧甘特图实例
  if (ganttInstance) {
    try {
      ganttInstance.destroy()
    } catch (e) {
      if (ganttRef.value) ganttRef.value.innerHTML = ''
    }
  }

  // 检查DOM元素是否存在
  if (!ganttRef.value) {
    ElMessage.error('甘特图容器未找到')
    return
  }

  // 初始化甘特图
  try {
    ganttInstance = new Gantt(ganttRef.value, ganttData, {
      header_height: 50,
      column_width: 60,
      step: 24,
      view_modes: ['Day', 'Week', 'Month'],
      bar_height: 20,
      bar_corner_radius: 4,
      arrow_curve: 5,
      padding: 18,
      date_format: 'YYYY-MM-DD',
      popup_trigger: 'click',
      custom_popup_html: (task) => {
        return `
          <div class="p-3 bg-white rounded-lg shadow-lg border border-gray-200">
            <h5 class="font-bold text-lg text-gray-800">${task.name}</h5>
            <p class="text-sm text-gray-600">进度：${task.progress}%</p>
            <p class="text-sm text-gray-600">时间：${task.start} - ${task.end}</p>
          </div>
        `
      }
    })
    ElMessage.success(`已加载${project.name}的甘特图`)
  } catch (err) {
    console.error('甘特图初始化失败：', err)
    ElMessage.error('甘特图初始化失败')
  }
}

// 修复：视图切换（兼容无change_view_mode方法的情况）
const changeView = (mode) => {
  if (!ganttInstance) return

  try {
    // 优先调用实例方法
    if (ganttInstance.change_view_mode) {
      ganttInstance.change_view_mode(mode)
    } else if (ganttInstance.setViewMode) {
      ganttInstance.setViewMode(mode)
    } else {
      // 兜底：重新初始化甘特图
      const newInstance = new Gantt(ganttRef.value, ganttData, {
        header_height: 50,
        column_width: 60,
        step: 24,
        view_modes: ['Day', 'Week', 'Month'],
        view_mode: mode, // 手动指定视图模式
        bar_height: 20,
        bar_corner_radius: 4,
        arrow_curve: 5,
        padding: 18,
        date_format: 'YYYY-MM-DD'
      })
      // 替换旧实例
      ganttInstance = newInstance
    }
    ElMessage.success(`切换为${mode}视图`)
  } catch (err) {
    console.error('切换视图失败：', err)
    ElMessage.error(`切换${mode}视图失败，请重试`)
  }
}

const loadDemoData = async () => {
  try {
    await axios.post(`${API_BASE}/projects/projects/create_demo/`)
    ElMessage.success('演示数据加载成功')
    loadProjects()
  } catch (error) {
    ElMessage.error('加载演示数据失败')
    console.error(error)
  }
}

const saveProject = async () => {
  try {
    if (editingProject.value) {
      await axios.put(`${API_BASE}/projects/projects/${editingProject.value.id}/`, projectForm)
      ElMessage.success('项目更新成功')
    } else {
      await axios.post(`${API_BASE}/projects/projects/`, projectForm)
      ElMessage.success('项目创建成功')
    }
    showCreateDialog.value = false
    loadProjects()
    resetProjectForm()
  } catch (error) {
    ElMessage.error(editingProject.value ? '项目更新失败' : '项目创建失败')
    console.error(error)
  }
}

const editProject = (project) => {
  editingProject.value = project
  Object.assign(projectForm, {
    name: project.name,
    description: project.description,
    start_date: project.start_date,
    end_date: project.end_date
  })
  showCreateDialog.value = true
}

const deleteProject = async (project) => {
  try {
    await ElMessageBox.confirm(`确定要删除项目 "${project.name}" 吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await axios.delete(`${API_BASE}/projects/projects/${project.id}/`)
    ElMessage.success('项目删除成功')
    loadProjects()
    if (selectedProject.value?.id === project.id) {
      handleBack() // 调用统一的返回方法
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('项目删除失败')
      console.error(error)
    }
  }
}

const tableRowClassName = ({ row }) => {
  return row.id === selectedProject.value?.id ? 'selected-row' : ''
}

const resetProjectForm = () => {
  Object.assign(projectForm, {
    name: '',
    description: '',
    start_date: '',
    end_date: ''
  })
  editingProject.value = null
}
</script>

<style scoped>
.project-management-container {
  padding: 20px;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  display: flex;
  gap: 20px;
  flex: 1;
  margin-top: 20px;
}

.project-list-section {
  flex: 1;
  min-width: 400px;
}

.project-detail-section {
  flex: 2;
  min-width: 600px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 日期选择器样式修复 */
:deep(.el-date-editor) {
  width: 100%;
}

:deep(.el-date-editor .el-input__inner) {
  width: 100%;
}

.selected-row {
  background-color: #ecf5ff !important;
}

/* 甘特图样式覆盖，适配Tailwind */
:deep(.gantt-task) {
  @apply rounded-md transition-all duration-200;
}
:deep(.gantt-task:hover) {
  @apply scale-[1.02];
}
:deep(.gantt-header) {
  @apply bg-gray-50 border-b border-gray-200;
}

/* 任务树样式优化 */
:deep(.el-tree) {
  @apply w-full h-full;
}
:deep(.el-tree-node__content) {
  @apply py-2 px-1;
}
:deep(.el-tree-node__expand-icon) {
  @apply mr-2;
}
</style>
