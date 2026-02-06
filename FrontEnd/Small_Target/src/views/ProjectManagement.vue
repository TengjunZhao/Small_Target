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
                <!-- 任务操作按钮 -->
                <div class="mb-4 flex gap-2">
                  <el-button type="primary" @click="showTaskDialog = true; editingTask = null; currentParentTask = null; resetTaskForm()">
                    新增任务
                  </el-button>
                  <el-button @click="refreshTaskTree">
                    刷新任务树
                  </el-button>
                </div>
                
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
                    <div class="flex items-center justify-between w-full py-1">
                      <div class="flex items-center flex-1 min-w-0">
                        <!-- 状态标签 -->
                        <el-tag 
                          :type="data.status === '已完成' ? 'success' : 
                                data.status === '进行中' ? 'warning' : 'info'" 
                          size="small" 
                          class="mr-2 flex-shrink-0"
                        >
                          {{ data.status }}
                        </el-tag>
                        
                        <!-- 任务名称 -->
                        <span class="font-medium truncate mr-2">{{ node.label }}</span>
                        
                        <!-- 优先级标签 -->
                        <el-tag 
                          v-if="data.priority"
                          :type="data.priority === 3 ? 'danger' : 
                                data.priority === 2 ? 'warning' : 'info'" 
                          size="small" 
                          effect="plain"
                          class="mr-2 flex-shrink-0"
                        >
                          {{ data.priority === 3 ? '高' : data.priority === 2 ? '中' : '低' }}优先级
                        </el-tag>
                        
                        <!-- 任务描述（如果存在且较短） -->
                        <span 
                          v-if="data.description && data.description.length <= 30" 
                          class="text-gray-500 text-sm truncate hidden sm:block"
                          :title="data.description"
                        >
                          {{ data.description }}
                        </span>
                      </div>
                      
                      <!-- 右侧信息 -->
                      <div class="flex items-center space-x-3 flex-shrink-0">
                        <!-- 进度 -->
                        <span class="text-sm text-gray-600 whitespace-nowrap">
                          进度：{{ data.progress }}%
                        </span>
                        
                        <!-- 时间信息 -->
                        <span 
                          v-if="data.start_date && data.end_date"
                          class="text-xs text-gray-400 hidden md:block"
                        >
                          {{ data.start_date }} 至 {{ data.end_date }}
                        </span>
                        
                        <!-- 操作按钮 -->
                        <div class="flex items-center space-x-1 flex-shrink-0">
                          <el-button 
                            type="primary" 
                            size="small" 
                            @click.stop="editTask(data)"
                            title="编辑任务"
                          >
                            编辑
                          </el-button>
                          <el-button 
                            type="success" 
                            size="small" 
                            @click.stop="addChildTask(data)"
                            title="添加子任务"
                          >
                            添加子任务
                          </el-button>
                          <el-button 
                            type="danger" 
                            size="small" 
                            @click.stop="deleteTask(data)"
                            title="删除任务"
                          >
                            删除
                          </el-button>
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
        <el-form-item label="项目负责人" prop="owner">
          <el-select v-model="projectForm.owner" placeholder="请选择项目负责人">
            <el-option label="管理员" :value="1" />
            <el-option label="用户1" :value="2" />
            <el-option label="用户2" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showCreateDialog = false">取消</el-button>
          <el-button type="primary" @click="saveProject">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 任务对话框 -->
    <el-dialog 
      v-model="showTaskDialog" 
      :title="editingTask ? '编辑任务' : (currentParentTask ? '添加子任务' : '新增任务')" 
      width="500px"
    >
      <el-form :model="taskForm" :rules="taskRules" ref="taskFormRef" label-width="100px">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="taskForm.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="taskForm.description" type="textarea" />
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker v-model="taskForm.start_date" type="date" placeholder="选择开始日期" />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker v-model="taskForm.end_date" type="date" placeholder="选择结束日期" />
        </el-form-item>
        <el-form-item label="持续天数" prop="duration">
          <el-input-number v-model="taskForm.duration" :min="1" />
        </el-form-item>
        <el-form-item label="进度" prop="progress">
          <el-slider v-model="taskForm.progress" :max="100" show-input />
        </el-form-item>
        <el-form-item label="优先级" prop="priority">
          <el-select v-model="taskForm.priority">
            <el-option label="低" :value="1" />
            <el-option label="中" :value="2" />
            <el-option label="高" :value="3" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showTaskDialog = false">取消</el-button>
          <el-button type="primary" @click="saveTask">保存</el-button>
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
  owner: 1  // 默认用户ID，实际应用中应该从认证系统获取
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
  duration: 1,
  progress: 0,
  priority: 2,
  parent: null
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

// 新增：甘特图数据状态
const ganttData = ref([])

// 新增：任务分解树数据（和甘特图数据联动）
const taskTreeData = ref([])

// 新增：树形组件配置
const treeProps = ref({
  label: 'label',
  children: 'children',
  isLeaf: (data) => !data.children || data.children.length === 0
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
  // 如果点击的是已选中的项目，则不重复加载
  if (selectedProject.value?.id === project.id) {
    return
  }

  selectedProject.value = project
  activeTab.value = 'gantt'

  await nextTick()

  // 销毁旧甘特图实例
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

  // 从后端获取甘特图数据
  try {
    const response = await axios.get(`${API_BASE}/projects/projects/${project.id}/gantt_data/`)
    const backendGanttData = response.data

    // 转换后端数据为frappe-gantt格式
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

    // 初始化甘特图
    ganttInstance = new Gantt(ganttRef.value, ganttData.value, {
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

    // 同时加载任务树数据
    await loadTaskTreeData(project.id)
  } catch (err) {
    console.error('甘特图初始化失败：', err)
    ElMessage.error('甘特图初始化失败')
    ganttData.value = []
    try {
      ganttInstance = new Gantt(ganttRef.value, [], { /* 空配置 */ })
    } catch (e) {}
  }
}

// 新增：加载任务树数据
const loadTaskTreeData = async (projectId) => {
  try {
    const response = await axios.get(`${API_BASE}/projects/projects/${projectId}/`)
    // 后端已经返回了完整的树形结构，直接使用
    const treeData = response.data.tasks || []
    
    // 直接赋值，因为后端已经构建好了树形结构
    taskTreeData.value = treeData
    
    // 强制触发响应式更新
    await nextTick()
    taskTreeData.value = [...taskTreeData.value]
    
    // 调试信息
    console.log('从后端获取的任务树数据:', taskTreeData.value)
    console.log('根节点数量:', taskTreeData.value.length)
    
    // 验证数据结构
    taskTreeData.value.forEach((node, index) => {
      console.log(`根节点 ${index}:`, {
        id: node.id,
        label: node.label,
        childrenCount: node.children ? node.children.length : 0,
        hasChildren: !!(node.children && node.children.length > 0)
      })
      
      // 如果有子节点，也打印子节点信息
      if (node.children && node.children.length > 0) {
        node.children.forEach((child, childIndex) => {
          console.log(`  子节点 ${childIndex}:`, {
            id: child.id,
            label: child.label,
            parent_id: child.parent_id,
            childrenCount: child.children ? child.children.length : 0
          })
        })
      }
    })
    
  } catch (error) {
    console.error('加载任务树数据失败：', error)
    taskTreeData.value = []
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



const saveProject = async () => {
  try {
    // 验证表单数据
    console.log('提交的项目数据:', projectForm);
    
    // 确保所有必需字段都有值
    const projectData = {
      name: projectForm.name.trim(),
      description: projectForm.description.trim() || '',
      start_date: projectForm.start_date,
      end_date: projectForm.end_date,
      owner: projectForm.owner
    };
    
    // 验证数据完整性
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
    
    console.log('发送的项目数据:', projectData);
    
    if (editingProject.value) {
      const response = await axios.put(`${API_BASE}/projects/projects/${editingProject.value.id}/`, projectData);
      console.log('项目更新响应:', response.data);
      ElMessage.success('项目更新成功');
    } else {
      const response = await axios.post(`${API_BASE}/projects/projects/`, projectData);
      console.log('项目创建响应:', response.data);
      ElMessage.success('项目创建成功');
    }
    
    showCreateDialog.value = false;
    await loadProjects();
    resetProjectForm();
  } catch (error) {
    const errorMessage = editingProject.value ? '项目更新失败' : '项目创建失败';
    ElMessage.error(errorMessage);
    console.error('项目保存错误:', error.response?.data || error.message);
    
    // 显示具体的错误信息
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
    end_date: '',
    owner: 1
  })
  editingProject.value = null
}

// 任务管理函数
const resetTaskForm = () => {
  Object.assign(taskForm, {
    name: '',
    description: '',
    start_date: '',
    end_date: '',
    duration: 1,
    progress: 0,
    priority: 2,
    parent: currentParentTask.value ? currentParentTask.value.id : null
  })
  editingTask.value = null
}

const refreshTaskTree = async () => {
  if (selectedProject.value) {
    await loadTaskTreeData(selectedProject.value.id)
    ElMessage.success('任务树已刷新')
  }
}

const editTask = (task) => {
  console.log('编辑任务:', task);
  editingTask.value = task;
  currentParentTask.value = null;
  
  // 填充表单数据
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
  
  console.log('填充后的表单数据:', taskForm);
  showTaskDialog.value = true;
  
  // 添加一个小延迟确保对话框完全渲染后再设置焦点
  setTimeout(() => {
    const nameInput = document.querySelector('.el-dialog input[placeholder="任务名称"]');
    if (nameInput) {
      nameInput.focus();
    }
  }, 100);
}

const addChildTask = (parentTask) => {
  console.log('添加子任务到:', parentTask);
  editingTask.value = null;
  currentParentTask.value = parentTask;
  resetTaskForm();
  showTaskDialog.value = true;
  
  // 设置父任务ID
  taskForm.parent = parentTask.id;
  
  // 添加延迟确保对话框渲染完成
  setTimeout(() => {
    const nameInput = document.querySelector('.el-dialog input[placeholder="任务名称"]');
    if (nameInput) {
      nameInput.focus();
    }
  }, 100);
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
    // 验证表单数据
    console.log('提交的任务表单:', taskForm);
    
    // 确保必需字段都有值
    const formatDate = (date) => {
      if (!date) return null;
      const d = new Date(date);
      const year = d.getFullYear();
      const month = String(d.getMonth() + 1).padStart(2, '0');
      const day = String(d.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    };
    
    const taskData = {
      name: taskForm.name.trim(),
      description: taskForm.description.trim() || '',
      start_date: formatDate(taskForm.start_date),
      end_date: formatDate(taskForm.end_date),
      duration: taskForm.duration || 1,
      progress: taskForm.progress || 0,
      priority: taskForm.priority || 2,
      project: selectedProject.value?.id,
      parent: taskForm.parent || null
    };
    
    // 验证数据完整性
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
    
    console.log('发送的任务数据:', taskData);
    
    let response;
    if (editingTask.value) {
      // 编辑任务
      response = await axios.put(`${API_BASE}/projects/tasks/${editingTask.value.id}/`, taskData);
      console.log('任务更新响应:', response.data);
      ElMessage.success('任务更新成功');
    } else {
      // 新增任务
      response = await axios.post(`${API_BASE}/projects/tasks/`, taskData);
      console.log('任务创建响应:', response.data);
      ElMessage.success('任务创建成功');
    }
    
    showTaskDialog.value = false;
    await refreshTaskTree();
    resetTaskForm();
  } catch (error) {
    const errorMessage = editingTask.value ? '任务更新失败' : '任务创建失败';
    ElMessage.error(errorMessage);
    console.error('任务保存错误:', error.response?.data || error.message);
    
    // 显示具体的错误信息
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
