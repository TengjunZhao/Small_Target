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

      <!-- 项目详情区域 -->
      <div v-if="selectedProject" class="project-detail-section">
        <el-tabs v-model="activeTab" type="border-card">
          <!-- 任务分解树 -->
          <el-tab-pane label="任务分解树" name="tree">
            <div class="tree-container">
              <div class="toolbar">
                <el-button type="primary" @click="addRootTask">添加根任务</el-button>
                <el-button @click="expandAll">展开全部</el-button>
                <el-button @click="collapseAll">收起全部</el-button>
              </div>
              <el-tree
                ref="taskTreeRef"
                :data="taskTreeData"
                node-key="id"
                :expanded-keys="expandedKeys"
                default-expand-all
                :props="treeProps"
                draggable
                @node-drop="handleNodeDrop"
                @node-contextmenu="showContextMenu"
              >
                <template #default="{ data }">
                  <div class="custom-tree-node">
                    <span>{{ data.name }}</span>
                    <span class="task-info">
                      <el-progress 
                        :percentage="data.progress" 
                        :stroke-width="8" 
                        style="width: 100px; margin: 0 10px;"
                      />
                      <el-tag :type="getStatusType(data.status)" size="small">
                        {{ data.status }}
                      </el-tag>
                      <el-dropdown @command="(command) => handleTaskAction(command, data)">
                        <el-button type="primary" link>
                          <el-icon><More /></el-icon>
                        </el-button>
                        <template #dropdown>
                          <el-dropdown-menu>
                            <el-dropdown-item command="add-child">添加子任务</el-dropdown-item>
                            <el-dropdown-item command="edit">编辑</el-dropdown-item>
                            <el-dropdown-item command="delete">删除</el-dropdown-item>
                            <el-dropdown-item command="update-progress">更新进度</el-dropdown-item>
                          </el-dropdown-menu>
                        </template>
                      </el-dropdown>
                    </span>
                  </div>
                </template>
              </el-tree>
            </div>
          </el-tab-pane>

          <!-- 甘特图 -->
          <el-tab-pane label="甘特图" name="gantt">
            <div class="gantt-container">
              <div class="gantt-toolbar">
                <el-button-group>
                  <el-button @click="zoomIn">放大</el-button>
                  <el-button @click="zoomOut">缩小</el-button>
                  <el-button @click="fitToScreen">适应屏幕</el-button>
                </el-button-group>
                <el-button type="primary" @click="refreshGantt">刷新数据</el-button>
              </div>
              
              <!-- 专业甘特图组件 -->
              <div class="professional-gantt">
                <GanttChart
                  :data="ganttData"
                  :dateRangeList="dateRangeList"
                  dateText="日期"
                  itemText="任务"
                  :options="ganttOptions"
                  @task-updated="handleTaskUpdated"
                  @task-clicked="handleTaskClicked"
                  style="height: 600px;"
                />
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
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

    <!-- 右键菜单 -->
    <div 
      v-show="contextMenuVisible" 
      class="context-menu" 
      :style="{ left: contextMenuX + 'px', top: contextMenuY + 'px' }"
    >
      <div class="context-menu-item" @click="addTaskFromContextMenu">添加任务</div>
      <div class="context-menu-item" @click="editTaskFromContextMenu">编辑任务</div>
      <div class="context-menu-item" @click="deleteTaskFromContextMenu">删除任务</div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { More } from '@element-plus/icons-vue'
import axios from 'axios'
import GanttChart from 'vue3-gantt'
import 'vue3-gantt/dist/style.css'

// 状态管理
const projects = ref([])
const selectedProject = ref(null)
const activeTab = ref('tree')
const showCreateDialog = ref(false)
const editingProject = ref(null)
const taskTreeData = ref([])

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

// 树形控件相关
const taskTreeRef = ref()
const expandedKeys = ref([])
const treeProps = {
  children: 'children',
  label: 'name'
}

// 右键菜单
const contextMenuVisible = ref(false)
const contextMenuX = ref(0)
const contextMenuY = ref(0)
const contextMenuNode = ref(null)

// 甘特图相关
const simpleGanttTasks = ref([])
const ganttTasks = ref([])
const ganttData = ref([])
const dateRangeList = ref([])
const ganttOptions = ref({
  viewMode: 'Day',
  dateFormat: 'YYYY-MM-DD',
  columnWidth: 60,
  barCornerRadius: 3,
  barHeight: 26,
  headerHeight: 50,
  locale: {
    code: 'zh',
    name: '中文',
    weekdays: ['周日', '周一', '周二', '周三', '周四', '周五', '周六'],
    months: ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'],
    week: '周',
    day: '天',
    month: '月'
  }
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

const loadProjects = async () => {
  try {
    const response = await axios.get(`${API_BASE}/projects/projects/`)
    // 确保返回的是数组格式
    projects.value = Array.isArray(response.data) ? response.data : []
  } catch (error) {
    ElMessage.error('加载项目列表失败')
    console.error(error)
    projects.value = [] // 设置为空数组以防错误
  }
}

const selectProject = (project) => {
  selectedProject.value = project
  loadProjectTasks(project.id)
}

const loadProjectTasks = async (projectId) => {
  try {
    console.log('Loading project tasks for ID:', projectId)
    const response = await axios.get(`${API_BASE}/projects/projects/${projectId}/`)
    console.log('Project data received:', response.data)
    taskTreeData.value = response.data.tasks || []
    console.log('Task tree data:', taskTreeData.value)
    
    // 处理简单甘特图数据
    const tasks = response.data.tasks || []
    simpleGanttTasks.value = tasks.map(task => ({
      id: task.id,
      name: task.name || `任务-${task.id}`,
      progress: task.progress || 0,
      start: task.start_date || '',
      end: task.end_date || ''
    }))
    
    // 处理专业甘特图数据 - 符合vue3-gantt要求的格式
    if (tasks.length > 0) {
      // 计算日期范围
      const allDates = tasks.flatMap(task => [task.start_date, task.end_date]).filter(Boolean)
      const startDate = allDates.length > 0 ? 
        allDates.reduce((min, date) => date < min ? date : min) : 
        new Date().toISOString().split('T')[0]
      
      const endDate = allDates.length > 0 ? 
        allDates.reduce((max, date) => date > max ? date : max) : 
        new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
      
      dateRangeList.value = [startDate, endDate]
      
      // 构造vue3-gantt需要的数据格式
      // 展开所有任务（包括子任务）到同一层级
      const flatTasks = []
      
      const flattenTasks = (taskList) => {
        taskList.forEach(task => {
          flatTasks.push({
            id: task.id,
            name: task.name || `任务-${task.id}`,
            description: task.description || '',
            start_date: task.start_date,
            end_date: task.end_date,
            progress: task.progress || 0,
            parent: task.parent
          })
          
          // 递归处理子任务
          if (task.children && task.children.length > 0) {
            flattenTasks(task.children)
          }
        })
      }
      
      flattenTasks(tasks)
      
      console.log('Flat tasks for gantt:', flatTasks)
      console.log('Date range:', dateRangeList.value)
      
      ganttData.value = [{
        type: 'normal',
        name: selectedProject.value?.name || '项目任务',
        schedule: flatTasks.map(task => ({
          id: task.id,
          name: task.name,
          desc: task.description || '',
          backgroundColor: task.progress >= 100 ? '#2ecc71' : task.progress > 0 ? '#3498db' : '#95a5a6',
          textColor: '#ffffff',
          days: [
            task.start_date || new Date().toISOString().split('T')[0],
            task.end_date || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
          ]
        }))
      }]
      
      console.log('Generated ganttData:', ganttData.value)
    } else {
      // 如果没有任务，设置默认日期范围
      const today = new Date().toISOString().split('T')[0]
      const nextMonth = new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]
      dateRangeList.value = [today, nextMonth]
      ganttData.value = [{
        type: 'normal',
        name: selectedProject.value?.name || '项目任务',
        schedule: []
      }]
    }
    
    // 保持原有的ganttTasks格式（用于其他可能的用途）
    ganttTasks.value = tasks.map(task => ({
      id: task.id.toString(),
      name: task.name || `任务-${task.id}`,
      start: task.start_date || new Date().toISOString().split('T')[0],
      end: task.end_date || new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      progress: task.progress || 0,
      dependencies: task.dependencies || '',
      custom_class: task.progress >= 100 ? 'completed' : task.progress > 0 ? 'in-progress' : 'not-started'
    }))
    
  } catch (error) {
    ElMessage.error('加载项目任务失败')
    console.error('Load project tasks error:', error)
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
  // 表单验证和保存逻辑
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
      selectedProject.value = null
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('项目删除失败')
      console.error(error)
    }
  }
}

const addRootTask = () => {
  // 添加根任务逻辑
  ElMessage.info('添加根任务功能待实现')
}

const expandAll = () => {
  // 获取所有节点的key并展开
  const allKeys = getAllNodeKeys(taskTreeData.value);
  expandedKeys.value = allKeys;
  ElMessage.success('已展开所有节点');
}

const collapseAll = () => {
  // 收起所有节点
  expandedKeys.value = [];
  ElMessage.success('已收起所有节点');
}

const getAllNodeKeys = (nodes) => {
  let keys = []
  nodes.forEach(node => {
    keys.push(node.id)
    if (node.children && node.children.length > 0) {
      keys = keys.concat(getAllNodeKeys(node.children))
    }
  })
  return keys
}

const handleNodeDrop = (draggingNode, dropNode, dropType) => {
  // 处理节点拖拽逻辑
  console.log('节点拖拽:', draggingNode, dropNode, dropType)
}

const showContextMenu = (event, data, node) => {
  event.preventDefault()
  contextMenuVisible.value = true
  contextMenuX.value = event.clientX
  contextMenuY.value = event.clientY
  contextMenuNode.value = { data, node }
}

const handleTaskAction = (command, task) => {
  switch (command) {
    case 'add-child':
      ElMessage.info('添加子任务功能待实现')
      break
    case 'edit':
      ElMessage.info('编辑任务功能待实现')
      break
    case 'delete':
      ElMessage.info('删除任务功能待实现')
      break
    case 'update-progress':
      updateTaskProgress(task)
      break
  }
}

const updateTaskProgress = async (task) => {
  try {
    const { value } = await ElMessageBox.prompt('请输入新的进度百分比 (0-100)', '更新进度', {
      inputValue: task.progress.toString(),
      inputPattern: /^(\d{1,2}(\.\d+)?|100)$/,
      inputErrorMessage: '请输入0-100之间的数字'
    })
    await axios.patch(`${API_BASE}/projects/tasks/${task.id}/update_progress/`, {
      progress: parseFloat(value)
    })
    ElMessage.success('进度更新成功')
    loadProjectTasks(selectedProject.value.id)
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('进度更新失败')
      console.error(error)
    }
  }
}

const getStatusType = (status) => {
  switch (status) {
    case '已完成': return 'success'
    case '进行中': return 'warning'
    case '未开始': return 'info'
    default: return 'info'
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

// 甘特图事件处理
const handleTaskUpdated = (task) => {
  console.log('任务更新:', task)
  // 验证task对象结构
  if (task && task.name) {
    ElMessage.success(`任务 "${task.name}" 已更新`)
    // 这里可以调用API更新任务数据
  } else {
    console.error('Invalid task object:', task)
    ElMessage.error('任务数据格式错误')
  }
}

const handleTaskClicked = (task) => {
  console.log('任务点击:', task)
  // 验证task对象结构
  if (task && task.name) {
    ElMessage.info(`点击了任务: ${task.name}`)
    // 可以在这里添加更多点击处理逻辑
  } else {
    console.error('Invalid task object:', task)
    ElMessage.error('任务数据格式错误')
  }
}

const refreshGantt = () => {
  if (selectedProject.value) {
    loadProjectTasks(selectedProject.value.id)
    ElMessage.success('甘特图数据已刷新')
  }
}

// 甘特图缩放控制方法
const zoomIn = () => {
  zoomLevel.value = Math.min(zoomLevel.value + 0.2, 3)
  ganttOptions.value.columnWidth = Math.round(60 * zoomLevel.value)
  ElMessage.info(`缩放级别: ${Math.round(zoomLevel.value * 100)}%`)
}

const zoomOut = () => {
  zoomLevel.value = Math.max(zoomLevel.value - 0.2, 0.5)
  ganttOptions.value.columnWidth = Math.round(60 * zoomLevel.value)
  ElMessage.info(`缩放级别: ${Math.round(zoomLevel.value * 100)}%`)
}

const fitToScreen = () => {
  zoomLevel.value = 1
  ganttOptions.value.columnWidth = 60
  ElMessage.success('已重置为100%缩放')
}

// 点击其他地方隐藏右键菜单
document.addEventListener('click', () => {
  contextMenuVisible.value = false
})
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

.tree-container {
  padding: 20px;
}

.toolbar {
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.task-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.gantt-container {
  padding: 20px;
}

.gantt-toolbar {
  margin-bottom: 20px;
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

/* WindiCSS 简单甘特图样式 */
.simple-gantt {
  padding: 20px;
}

.gantt-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 8px;
  border-radius: 4px;
  background-color: #f8f9fa;
}

.task-name {
  width: 200px;
  font-weight: 500;
  color: #333;
}

.task-timeline {
  flex: 1;
  position: relative;
  height: 20px;
  background-color: #e9ecef;
  border-radius: 3px;
  overflow: hidden;
}

.task-bar {
  position: relative;
  height: 100%;
  transition: width 0.3s ease;
}

.task-progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 12px;
  font-weight: bold;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

/* 树形控件修复后的样式 */
.context-menu {
  position: fixed;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
  z-index: 1000;
}

.context-menu-item {
  padding: 8px 16px;
  cursor: pointer;
  border-bottom: 1px solid #eee;
}

.context-menu-item:hover {
  background-color: #f5f5f5;
}

.context-menu-item:last-child {
  border-bottom: none;
}

.selected-row {
  background-color: #ecf5ff !important;
}

:deep(.el-tree-node__content) {
  height: auto;
  padding: 10px 0;
}

:deep(.el-tree-node__label) {
  flex: 1;
}
</style>