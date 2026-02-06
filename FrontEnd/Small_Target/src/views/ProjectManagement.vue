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

      <!-- 项目详情区域 - 移除甘特图，保留任务分解树并标记待开发 -->
      <div v-if="selectedProject" class="project-detail-section">
        <el-card class="box-card">
          <template #header>
            <span>项目详情：{{ selectedProject.name }}（功能待开发）</span>
          </template>
          <div class="under-development">
            <el-empty
              description="该模块功能正在开发中，敬请期待！"
              :image-size="120"
            >
              <el-button type="primary" @click="selectedProject = null">返回项目列表</el-button>
            </el-empty>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox, ElEmpty } from 'element-plus'
import axios from 'axios'

// 状态管理
const projects = ref([])
const selectedProject = ref(null)
const showCreateDialog = ref(false)
const editingProject = ref(null)

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
  // 移除加载任务的逻辑（甘特图/任务树相关）
  ElMessage.info(`已选择项目：${project.name}，详情功能待开发`)
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
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.under-development {
  width: 100%;
  height: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
</style>
