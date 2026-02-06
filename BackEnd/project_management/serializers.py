from rest_framework import serializers
from .models import Project, Task, TaskDependency

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    parent_id = serializers.PrimaryKeyRelatedField(source='parent', read_only=True)
    
    class Meta:
        model = Task
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class TaskDependencySerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskDependency
        fields = '__all__'

class ProjectDetailSerializer(serializers.ModelSerializer):
    """项目详情序列化器，包含完整的任务树结构"""
    tasks = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'
    
    def get_tasks(self, obj):
        # 获取所有任务
        all_tasks = obj.tasks.all()
        # 构建任务字典以便快速查找
        task_dict = {task.id: task for task in all_tasks}
        
        # 序列化所有任务
        serializer = TaskSerializer(all_tasks, many=True)
        task_data = serializer.data
        
        # 为每个任务添加子任务列表
        task_map = {task['id']: task for task in task_data}
        
        for task in task_data:
            task['children'] = []
            # 查找当前任务的所有子任务
            for child_task in all_tasks:
                if child_task.parent_id == task['id']:
                    child_data = TaskSerializer(child_task).data
                    child_data['children'] = []
                    task['children'].append(child_data)
        
        # 只返回根任务（没有父任务的任务）
        root_tasks = [task for task in task_data if not task['parent_id']]
        return root_tasks