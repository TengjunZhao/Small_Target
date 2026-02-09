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
                <el-icon><Plus /></el-icon>
                <span class="btn-text">新建项目</span>
              </el-button>
            </div>
          </template>

          <el-table
            :data="projects"
            style="width: 100%"
            @row-click="selectProject"
            :row-class-name="tableRowClassName"
            highlight-current-row
            :fit="true"
            size="small"
          >
            <el-table-column prop="name" label="项目名称" min-width="120" />
            <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip>
              <template #default="scope">
                <span class="truncate-text">{{ scope.row.description }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="start_date" label="开始日期" width="100" />
            <el-table-column prop="end_date" label="结束日期" width="100" />
            <el-table-column label="状态" width="80">
              <template #default="scope">
                <el-tag :type="scope.row.is_active ? 'success' : 'info'" size="small">
                  {{ scope.row.is_active ? '进行中' : '已结束' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="scope">
                <!-- 用 flex 容器包裹两个按钮，确保水平排列 -->
                <div class="table-operation-buttons">
                  <el-button size="small" @click.stop="editProject(scope.row)">
                    <el-icon><Edit /></el-icon>
                    <span class="btn-text">编辑</span>
                  </el-button>
                  <el-button size="small" type="danger" @click.stop="deleteProject(scope.row)">
                    <el-icon><Delete /></el-icon>
                    <span class="btn-text">删除</span>
                  </el-button>
                </div>
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
          <el-tabs v-model="activeTab" class="w-full" type="card">
            <!-- 甘特图选项卡 -->
            <el-tab-pane label="甘特图" name="gantt">
              <div class="gantt-container">
                <div class="gantt-toolbar">
                  <span class="gantt-title">项目进度甘特图</span>
                    <div class="gantt-view-buttons">
                      <el-button @click="changeView('Day')" size="small">
                        <el-icon><Calendar /></el-icon>
                        <span class="btn-text">日视图</span>
                      </el-button>
                      <el-button @click="changeView('Month')" size="small">
                        <el-icon><Calendar /></el-icon>
                        <span class="btn-text">月视图</span>
                      </el-button>
                    </div>
                </div>
                <div ref="ganttRef" class="gantt-content"></div>
              </div>
            </el-tab-pane>

            <!-- 任务分解树选项卡 -->
            <el-tab-pane label="任务分解树" name="taskTree">
              <div class="task-tree-container">
                <!-- 任务操作按钮 -->
                <div class="mb-4 flex gap-2 flex-wrap">
                  <!-- 冲突解决：保留带图标、size的按钮样式，保持UI统一 -->
                  <el-button type="primary" size="small" @click="showTaskDialog = true; editingTask = null; currentParentTask = null; resetTaskForm()">
                    <el-icon><Plus /></el-icon>
                    <span class="btn-text">新增任务</span>
                  </el-button>
                  <el-button size="small" @click="refreshTaskTree">
                    <el-icon><Refresh /></el-icon>
                    <span class="btn-text">刷新</span>
                  </el-button>
                  <el-button @click="expandAllNodes">
                    展开全部
                  </el-button>
                  <el-button @click="collapseAllNodes">
                    折叠全部
                  </el-button>
                  <el-button @click="console.log('当前展开的节点:', expandedKeys.value)">
                    查看展开状态
                  </el-button>
                </div>

                <!-- 任务树形组件 -->
                <el-tree
                  :data="taskTreeData"
                  :props="treeProps"
                  node-key="id"
                  :default-expanded-keys="expandedKeys"
                  class="task-tree-content"
                  :expand-on-click-node="false"
                  size="small"
                  @node-expand="handleNodeExpand"
                  @node-collapse="handleNodeCollapse"
                >
                  <!-- 自定义树形节点内容 -->
                  <template #default="{ node, data }">
                    <div class="tree-node-content">
                      <div class="node-left">
                        <!-- 状态标签 -->
                        <el-tag
                          :type="data.status === '已完成' ? 'success' :
                                data.status === '进行中' ? 'warning' : 'info'"
                          size="small"
                          class="mr-2"
                        >
                          {{ data.status }}
                        </el-tag>

                        <!-- 任务名称 -->
                        <span class="font-medium truncate" :title="node.label + (data.description ? ' - ' + data.description : '')">{{ node.label }}</span>

                        <!-- 优先级标签（移动端隐藏） -->
                        <el-tag
                          v-if="data.priority"
                          :type="data.priority === 3 ? 'danger' :
                                data.priority === 2 ? 'warning' : 'info'"
                          size="small"
                          effect="plain"
                          class="ml-2 priority-tag"
                        >
                          {{ data.priority === 3 ? '高' : data.priority === 2 ? '中' : '低' }}
                        </el-tag>
                      </div>

                      <!-- 右侧信息 -->
                      <div class="node-right">
                        <!-- 进度（简化显示） -->
                        <span class="text-xs progress-text">
                          {{ data.progress }}%
                        </span>

                        <!-- 操作按钮 -->
                        <div class="node-actions">
                          <el-button
                            type="primary"
                            size="small"
                            @click.stop="editTask(data)"
                            icon="Edit"
                            circle
                            title="编辑任务"
                          />
                          <el-button
                            type="success"
                            size="small"
                            @click.stop="addChildTask(data)"
                            icon="Plus"
                            circle
                            title="添加子任务"
                          />
                          <el-button
                            type="danger"
                            size="small"
                            @click.stop="deleteTask(data)"
                            icon="Delete"
                            circle
                            title="删除任务"
                          />
                        </div>
                      </div>
                    </div>
                  </template>
                </el-tree>
              </div>
            </el-tab-pane>
          </el-tabs>

          <!-- 返回按钮 -->
          <div class="mt-4 flex justify-end">
            <el-button type="primary" size="small" @click="handleBack">
              <el-icon><ArrowLeft /></el-icon>
              <span class="btn-text">返回列表</span>
            </el-button>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 创建/编辑项目对话框 -->
    <el-dialog v-model="showCreateDialog" :title="editingProject ? '编辑项目' : '新建项目'" width="90%" max-width="500px">
      <el-form :model="projectForm" :rules="projectRules" ref="projectFormRef" label-width="80px" size="small">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="projectForm.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="projectForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="projectForm.start_date" type="date" placeholder="选择开始日期" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="projectForm.end_date" type="date" placeholder="选择结束日期" />
        </el-form-item>
        <el-form-item label="负责人" prop="owner">
          <el-select v-model="projectForm.owner" placeholder="选择负责人">
            <el-option label="管理员" :value="1" />
            <el-option label="用户1" :value="2" />
            <el-option label="用户2" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button size="small" @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" size="small" @click="saveProject">保存</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 任务对话框 -->
    <el-dialog
      v-model="showTaskDialog"
      :title="editingTask ? '编辑任务' : (currentParentTask ? '添加子任务' : '新增任务')"
      width="90%"
      max-width="500px"
    >
      <el-form :model="taskForm" :rules="taskRules" ref="taskFormRef" label-width="80px" size="small">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="taskForm.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="taskForm.start_date" type="date" placeholder="选择开始日期" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="taskForm.end_date" type="date" placeholder="选择结束日期" />
        </el-form-item>
        <el-form-item label="持续天数">
          <el-input
            :value="taskForm.duration + ' 天'"
            readonly
            size="small"
            placeholder="根据日期自动计算"
          >
            <template #suffix>
              <span class="text-gray-400 text-xs">自动计算</span>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="进度" prop="progress">
          <el-slider v-model="taskForm.progress" :max="100" show-input size="small" />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="taskForm.priority" size="small">
            <el-option label="低" :value="1" />
            <el-option label="中" :value="2" />
            <el-option label="高" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button size="small" @click="showTaskDialog = false">取消</el-button>
          <el-button type="primary" size="small" @click="saveTask">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, Refresh, Calendar, ArrowLeft } from '@element-plus/icons-vue'
import {formatDateForDatabase } from '@/utils/dateUtils.js'
import axios from 'axios'
import Gantt from 'frappe-gantt'
import '../assets/frappe-gantt.css'

// 状态管理
const projects = ref([])
const selectedProject = ref(null)
const showCreateDialog = ref(false)
const editingProject = ref(null)
const activeTab = ref('gantt')

// 任务管理状态
const showTaskDialog = ref(false)
const editingTask = ref(null)
const currentParentTask = ref(null)
const taskFormRef = ref(null)

// 表单相关
const projectForm = reactive({
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  owner: 1
})

const projectRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  start_date: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  end_date: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
  owner: [{ required: true, message: '请选择项目负责人', trigger: 'change' }]
}

// 任务表单
const taskForm = reactive({
  id: null,
  name: '',
  description: '',
  start_date: '',
  end_date: '',
  duration: 1,  // 将由计算得出
  progress: 0,
  priority: 2,
  parent: null
})

// 计算任务持续天数的函数
const calculateDuration = (startDate, endDate) => {
  if (!startDate || !endDate) return 1;

  try {
    const start = new Date(startDate);
    const end = new Date(endDate);

    // 计算天数差（包括起始和结束日期）
    const timeDiff = end.getTime() - start.getTime();
    const dayDiff = Math.ceil(timeDiff / (1000 * 3600 * 24)) + 1;

    return Math.max(1, dayDiff); // 至少1天
  } catch (error) {
    console.error('计算持续时间出错:', error);
    return 1;
  }
}

// 监听日期变化自动计算duration
watch([() => taskForm.start_date, () => taskForm.end_date], ([newStart, newEnd]) => {
  if (newStart && newEnd) {
    taskForm.duration = calculateDuration(newStart, newEnd);
  }
})

// 任务表单验证规则
const taskRules = {
  name: [
    { required: true, message: '请输入任务名称', trigger: 'blur' }
  ],
  start_date: [
    { required: true, message: '请选择开始日期', trigger: 'change' }
  ],
  end_date: [
    { required: true, message: '请选择结束日期', trigger: 'change' }
  ]
}

// 甘特图核心配置
const ganttRef = ref(null)
let ganttInstance = null
const ganttData = ref([])
const taskTreeData = ref([])
const treeProps = ref({
  label: 'name',
  children: 'children',
  isLeaf: (data) => !data.children || data.children.length === 0
})

// 新增：树形组件展开状态管理（遵循内存中的最佳实践）
const expandedKeys = ref([])

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

const handleBack = () => {
  selectedProject.value = null
  activeTab.value = 'gantt'
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
  if (selectedProject.value?.id === project.id) return

  selectedProject.value = project
  activeTab.value = 'gantt'
  await nextTick()

  if (ganttInstance) {
    try {
      ganttInstance.destroy()
    } catch (e) {
      if (ganttRef.value) ganttRef.value.innerHTML = ''
    }
  }

  if (!ganttRef.value) {
    ElMessage.error('甘特图容器未找到')
    return
  }

  try {
    const response = await axios.get(`${API_BASE}/projects/projects/${project.id}/gantt_data/`)
    const backendGanttData = response.data
    const formattedGanttData = backendGanttData.map(task => ({
      id: task.id.toString(),
      name: task.name,
      start: task.start_date,
      end: task.end_date,
      progress: task.progress || 0,
      custom_class: task.status === 'completed' ? 'bg-green-500' :
                  task.progress > 0 ? 'bg-yellow-500' : 'bg-blue-500'
    }))

    ganttData.value = formattedGanttData
    ganttInstance = new Gantt(ganttRef.value, ganttData.value, {
      header_height: 40, // 移动端缩小头部高度
      column_width: 50,
      step: 24,
      view_modes: ['Day', 'Week', 'Month'],
      bar_height: 18,
      bar_corner_radius: 4,
      arrow_curve: 5,
      padding: 10,
      date_format: 'YYYY-MM-DD',
      popup_trigger: 'click',
      custom_popup_html: (task) => {
        return `
          <div class="p-2 bg-white rounded-lg shadow-lg border border-gray-200 text-sm">
            <h5 class="font-bold text-gray-800">${task.name}</h5>
            <p class="text-xs text-gray-600">进度：${task.progress}%</p>
            <p class="text-xs text-gray-600">时间：${task.start} - ${task.end}</p>
          </div>
        `
      }
    })
    ElMessage.success(`已加载${project.name}的甘特图`)
    await loadTaskTreeData(project.id)
  } catch (err) {
    console.error('甘特图初始化失败：', err)
    ElMessage.error('甘特图初始化失败')
    ganttData.value = []
    try {
      ganttInstance = new Gantt(ganttRef.value, [], {})
    } catch (e) {}
  }
}

const loadTaskTreeData = async (projectId) => {
  try {
    const response = await axios.get(`${API_BASE}/projects/projects/${projectId}/`)
    // 冲突解决：保留完整的数据转换和展开状态管理逻辑
    // 后端已经返回了完整的树形结构，直接使用
    let treeData = response.data.tasks || []

    // 数据转换：将后端的 name 字段转换为前端需要的 label 字段
    const convertTaskData = (tasks) => {
      return tasks.map(task => {
        // 创建新对象，保留原有属性
        const convertedTask = {
          ...task,
          label: task.name || task.label || '未命名任务', // 使用name作为label
          children: task.children ? convertTaskData(task.children) : []
        }
        return convertedTask
      })
    }

    treeData = convertTaskData(treeData)

    // 直接赋值，因为后端已经构建好了树形结构
    taskTreeData.value = treeData
    await nextTick()
    taskTreeData.value = [...taskTreeData.value]

    // 调试信息
    console.log('从后端获取的任务树数据:', taskTreeData.value)
    console.log('根节点数量:', taskTreeData.value.length)

    // 计算并显示树的深度
    const treeDepth = calculateTreeDepth(taskTreeData.value)
    console.log('任务树最大深度:', treeDepth)

    // 初始化展开状态 - 展开前两层节点
    expandedKeys.value = []
    const collectExpandedKeys = (nodes, maxDepth = 2, currentDepth = 0) => {
      if (!nodes || currentDepth >= maxDepth) return

      for (const node of nodes) {
        if (currentDepth < maxDepth - 1) {
          expandedKeys.value.push(node.id)
        }
        if (node.children && node.children.length > 0) {
          collectExpandedKeys(node.children, maxDepth, currentDepth + 1)
        }
      }
    }

    collectExpandedKeys(taskTreeData.value)
    console.log('初始展开的节点keys:', expandedKeys.value)

    // 验证数据结构
    const validateTreeStructure = (nodes, level = 0, parentId = null) => {
      if (!nodes) return

      nodes.forEach((node, index) => {
        const indent = '  '.repeat(level)
        console.log(`${indent}节点 [${level}] ${index}:`, {
          id: node.id,
          label: node.label,
          name: node.name,
          parent_id: node.parent_id,
          parentIdCheck: node.parent_id === parentId,
          childrenCount: node.children ? node.children.length : 0,
          hasChildren: !!(node.children && node.children.length > 0)
        })

        // 递归验证子节点
        if (node.children && node.children.length > 0) {
          validateTreeStructure(node.children, level + 1, node.id)
        }
      })
    }

    console.log('=== 任务树结构验证 ===')
    validateTreeStructure(taskTreeData.value)
  } catch (error) {
    console.error('加载任务树数据失败：', error)
    taskTreeData.value = []
  }
}

const changeView = (mode) => {
  if (!ganttInstance) return
  try {
    if (ganttInstance.change_view_mode) {
      ganttInstance.change_view_mode(mode)
    } else if (ganttInstance.setViewMode) {
      ganttInstance.setViewMode(mode)
    } else {
      const newInstance = new Gantt(ganttRef.value, ganttData, {
        header_height: 40,
        column_width: 50,
        step: 24,
        view_modes: ['Day', 'Week', 'Month'],
        view_mode: mode,
        bar_height: 18,
        bar_corner_radius: 4,
        arrow_curve: 5,
        padding: 10,
        date_format: 'YYYY-MM-DD'
      })
      ganttInstance = newInstance
    }
    ElMessage.success(`切换为${mode}视图`)
  } catch (err) {
    console.error('切换视图失败：', err)
    ElMessage.error(`切换${mode}视图失败，请重试`)
  }
}

const saveProject = async () => {
  try {
    const projectData = {
      name: projectForm.name.trim(),
      description: projectForm.description.trim() || '',
      start_date: formatDateForDatabase(projectForm.start_date),
      end_date: formatDateForDatabase(projectForm.end_date),
      owner: projectForm.owner
    };

    if (!projectData.name) {
      ElMessage.error('项目名称不能为空');
      return;
    }
    if (!projectData.start_date || !projectData.end_date) {
      ElMessage.error('请填写完整的日期信息');
      return;
    }
    if (!projectData.owner) {
      ElMessage.error('请选择项目负责人');
      return;
    }

    if (editingProject.value) {
      await axios.put(`${API_BASE}/projects/projects/${editingProject.value.id}/`, projectData);
      ElMessage.success('项目更新成功');
    } else {
      await axios.post(`${API_BASE}/projects/projects/`, projectData);
      ElMessage.success('项目创建成功');
    }

    showCreateDialog.value = false;
    await loadProjects();
    resetProjectForm();
  } catch (error) {
    const errorMessage = editingProject.value ? '项目更新失败' : '项目创建失败';
    ElMessage.error(errorMessage);
    console.error('项目保存错误:', error.response?.data || error.message);
    if (error.response?.data) {
      const errorDetails = error.response.data;
      if (typeof errorDetails === 'object') {
        Object.keys(errorDetails).forEach(key => {
          const fieldErrors = errorDetails[key];
          if (Array.isArray(fieldErrors)) {
            ElMessage.error(`${key}: ${fieldErrors.join(', ')}`);
          }
        });
      }
    }
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
      handleBack()
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
    end_date: '',
    owner: 1
  })
  editingProject.value = null
}

const resetTaskForm = () => {
  console.log('=== resetTaskForm 调试 ===');
  console.log('调用时 currentParentTask:', currentParentTask.value);

  // 保存当前的parent值
  const currentParentId = currentParentTask.value ? currentParentTask.value.id : null;
  console.log('保存的 currentParentId:', currentParentId);

  Object.assign(taskForm, {
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    duration: 1,
    progress: 0,
    priority: 2,
    parent: currentParentId  // 使用保存的parent值
  });

  console.log('resetTaskForm 后 taskForm:', taskForm);
  editingTask.value = null;
}

const refreshTaskTree = async () => {
  if (selectedProject.value) {
    await loadTaskTreeData(selectedProject.value.id)
    ElMessage.success('任务树已刷新')
  }
}

// 新增：树节点展开处理
const handleNodeExpand = (data) => {
  console.log('节点展开:', data.id, data.label)
  if (!expandedKeys.value.includes(data.id)) {
    expandedKeys.value.push(data.id)
  }
}

// 新增：树节点折叠处理
const handleNodeCollapse = (data) => {
  console.log('节点折叠:', data.id, data.label)
  const index = expandedKeys.value.indexOf(data.id)
  if (index > -1) {
    expandedKeys.value.splice(index, 1)
  }
}

// 新增：计算树的最大深度（用于调试）
const calculateTreeDepth = (nodes, currentDepth = 0) => {
  if (!nodes || nodes.length === 0) return currentDepth

  let maxDepth = currentDepth
  for (const node of nodes) {
    const depth = calculateTreeDepth(node.children, currentDepth + 1)
    maxDepth = Math.max(maxDepth, depth)
  }
  return maxDepth
}

const editTask = (task) => {
  editingTask.value = task;
  currentParentTask.value = null;
  Object.assign(taskForm, {
    name: task.label || task.name || '',
    description: task.description || '',
    start_date: task.start_date || '',
    end_date: task.end_date || '',
    duration: task.duration || 1,
    progress: task.progress || 0,
    priority: task.priority || 2,
    parent: task.parent_id || null
  });
  showTaskDialog.value = true;
  setTimeout(() => {
    const nameInput = document.querySelector('.el-dialog input[placeholder="任务名称"]');
    if (nameInput) nameInput.focus();
  }, 100);
}

const addChildTask = (parentTask) => {
  editingTask.value = null;
  currentParentTask.value = parentTask;

  console.log('设置 currentParentTask 后:', currentParentTask.value);
  console.log('准备设置 taskForm.parent:', parentTask.id);

  // 先设置parent，再重置表单，确保parent值不会被覆盖
  taskForm.parent = parentTask.id;
  resetTaskForm();
  // 确保duration字段保持正确的默认值
  taskForm.duration = 1;
  showTaskDialog.value = true;
  console.log('最终 taskForm 状态:', taskForm);
  setTimeout(() => {
    const nameInput = document.querySelector('.el-dialog input[placeholder="任务名称"]');
    if (nameInput) nameInput.focus();
  }, 100);
}

// 新增：手动展开/折叠所有节点的功能
const expandAllNodes = () => {
  const collectAllKeys = (nodes) => {
    const keys = []
    const traverse = (nodeList) => {
      if (!nodeList) return
      nodeList.forEach(node => {
        keys.push(node.id)
        if (node.children && node.children.length > 0) {
          traverse(node.children)
        }
      })
    }
    traverse(nodes)
    return keys
  }

  expandedKeys.value = collectAllKeys(taskTreeData.value)
  ElMessage.success('已展开所有节点')
}

const collapseAllNodes = () => {
  expandedKeys.value = []
  ElMessage.success('已折叠所有节点')
}

const deleteTask = async (task) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除任务 "${task.label || task.name}" 吗？`,
      '确认删除',
      { type: 'warning' }
    )
    await axios.delete(`${API_BASE}/projects/tasks/${task.id}/`)
    ElMessage.success('任务删除成功')
    await refreshTaskTree()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('任务删除失败')
      console.error(error)
    }
  }
}

const saveTask = async () => {
  try {
    // 确保duration字段有有效值
    const durationValue = taskForm.duration && taskForm.duration > 0 ? taskForm.duration : 1;

    const taskData = {
      name: taskForm.name.trim(),
      description: taskForm.description.trim() || '',
      start_date: formatDateForDatabase(taskForm.start_date),
      end_date: formatDateForDatabase(taskForm.end_date),
      duration: durationValue,  // 使用确保有效的duration值
      progress: taskForm.progress || 0,
      priority: taskForm.priority || 2,
      project: selectedProject.value?.id,
      parent: taskForm.parent || null  // 关键字段
    };

    if (!taskData.name) {
      ElMessage.error('任务名称不能为空');
      return;
    }
    if (!taskData.start_date || !taskData.end_date) {
      ElMessage.error('请填写完整的日期信息');
      return;
    }
    if (!taskData.project) {
      ElMessage.error('未选择项目，请先选择一个项目');
      return;
    }
    if (new Date(taskData.start_date) > new Date(taskData.end_date)) {
      ElMessage.error('开始日期不能晚于结束日期');
      return;
    }

    if (editingTask.value) {
      await axios.put(`${API_BASE}/projects/tasks/${editingTask.value.id}/`, taskData);
      ElMessage.success('任务更新成功');
    } else {
      console.log('发送的任务数据:', taskData);  // 调试信息
      await axios.post(`${API_BASE}/projects/tasks/`, taskData);
      ElMessage.success('任务创建成功');
    }

    showTaskDialog.value = false;
    await refreshTaskTree();
    resetTaskForm();
  } catch (error) {
    const errorMessage = editingTask.value ? '任务更新失败' : '任务创建失败';
    ElMessage.error(errorMessage);
    console.error('任务保存错误:', error.response?.data || error.message);
    // 显示详细的错误信息
    if (error.response?.data) {
      const errorDetails = error.response.data;
      if (typeof errorDetails === 'object') {
        Object.keys(errorDetails).forEach(key => {
          const fieldErrors = errorDetails[key];
          if (Array.isArray(fieldErrors)) {
            ElMessage.error(`${key}: ${fieldErrors.join(', ')}`);
          }
        });
      } else {
        ElMessage.error(`错误详情: ${JSON.stringify(errorDetails)}`);
      }
    }
  }
}
</script>

<style scoped>
.project-management-container {
  padding: 10px; /* 移动端缩小内边距 */
  height: 100vh;
  display: flex;
  flex-direction: column;
  box-sizing: border-box; /* 防止padding导致溢出 */
  overflow: auto; /* 允许整体滚动 */
}

.main-content {
  display: flex;
  gap: 15px;
  flex: 1;
  margin-top: 15px;
  overflow: auto;
}

/* 项目列表区域响应式 */
.project-list-section {
  flex: 1;
  min-width: 280px; /* 移动端最小宽度 */
  max-width: 100%;
}
:deep(.project-list-section .el-card) {
  display: flex;
  flex-direction: column;
  height: 100%;
}
:deep(.project-list-section .el-card__body) {
  flex: 1;
  overflow: auto; /* 列表内容超出时滚动 */
  padding: 16px;
}
/* 项目详情区域响应式 */
.project-detail-section {
  flex: 1; /* 移动端和列表等分 */
  min-width: 280px;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%; /* 填充main-content高度 */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* 甘特图容器响应式 */
.gantt-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%; /* 填充选项卡高度 */
  padding: 4px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px #eee;
  box-sizing: border-box;
}

.gantt-toolbar {
  display: flex;
  justify-content: space-between; /* 标题左，按钮右 */
  align-items: center;
  padding: 8px 4px;
  margin-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.gantt-title {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.gantt-view-buttons {
  display: flex;
  gap: 8px; /* 按钮之间的间距 */
}

.gantt-content {
  flex: 1; /* 自动填充容器剩余高度 */
  width: 100%;
  min-height: 200px; /* 最小高度，避免内容为空时塌陷 */
  overflow: auto; /* 甘特图内容超出时横向/纵向滚动 */
}
@media (max-width: 768px) {
  .gantt-toolbar {
    padding: 4px 2px;
    margin-bottom: 4px;
  }
  .gantt-title {
    font-size: 12px;
  }
  .gantt-view-buttons .btn-text {
    display: none;
  }
  .gantt-content {
    min-height: 150px;
  }
}
/* 任务树容器响应式 */
.task-tree-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  height: 100%; /* 填充选项卡高度 */
  padding: 4px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 1px 2px #eee;
  box-sizing: border-box;
}

.task-tree-content {
  flex: 1; /* 自动填充剩余高度 */
  width: 100%;
  min-height: 200px; /* 最小高度 */
  overflow: auto; /* 任务树内容超出时滚动 */
}

/* 树形节点样式优化 */
.tree-node-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 2px 0;
}

.node-left {
  display: flex;
  align-items: center;
  flex: 1;
  min-width: 0; /* 解决文字溢出 */
  gap: 8px;
}

.node-right {
  display: flex;
  align-items: center;
  gap: 8px;
}

.node-actions {
  display: flex;
  gap: 4px;
}

/* 文字截断 */
.truncate-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* 表格操作按钮容器 */
.table-operation-buttons {
  display: flex;
  gap: 8px;
  align-items: center;
}

.selected-row {
  background-color: #ecf5ff !important;
}

/* 日期选择器样式修复 */
:deep(.el-date-editor) {
  width: 100%;
}

:deep(.el-date-editor .el-input__inner) {
  width: 100%;
}

/* 甘特图样式覆盖 */
:deep(.gantt-task) {
  border-radius: 4px;
  transition: all 0.2s;
}
:deep(.gantt-task:hover) {
  transform: scale(1.02);
}
:deep(.gantt-header) {
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
}

/* 媒体查询 - 平板 (768px以下) */
@media (max-width: 768px) {
  .main-content {
    flex-direction: column; /* 垂直排列 */
    gap: 10px;
  }

  .gantt-container, .task-tree-container {
    height: 300px; /* 平板缩小高度 */
  }

  /* 隐藏优先级文字，只留图标 */
  .priority-tag {
    display: none;
  }

  /* 隐藏按钮文字，只留图标 */
  .btn-text {
    display: none;
  }

  /* 进度文字简化 */
  .progress-text {
    font-size: 10px;
  }
}

/* 媒体查询 - 手机 (480px以下) */
@media (max-width: 480px) {
  .main-content {
    flex-direction: column; /* 垂直排列 */
    gap: 10px;
  }

  .project-management-container {
    padding: 5px;
  }

  .gantt-container, .task-tree-container {
    height: 100%; /* 手机进一步缩小高度 */
  }

  /* 表格列优化 */
  :deep(.el-table-column--width-100) {
    width: 80px !important;
  }

  :deep(.el-table-column--width-80) {
    width: 60px !important;
  }

  /* 树形节点进一步简化 */
  .node-left {
    gap: 4px;
  }

  .node-actions {
    gap: 2px;
  }
}
.table-operation-buttons {
  display: flex;
  gap: 8px; /* 按钮之间的间距 */
  white-space: nowrap; /* 禁止按钮内文字换行 */
  align-items: center; /* 垂直居中对齐 */
}

/* 可选：响应式隐藏按钮文字（小屏幕只显示图标） */
@media (max-width: 768px) {
  .btn-text {
    display: none;
  }
  .table-operation-buttons {
    gap: 4px;
  }
}
</style>
