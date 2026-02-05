from rest_framework import serializers
from .models import Project, Task, TaskDependency

class TaskSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField()
    is_completed = serializers.ReadOnlyField()
    
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
        # 获取根任务（没有父任务的任务）
        root_tasks = obj.tasks.filter(parent=None)
        return self._serialize_task_tree(root_tasks)
    
    def _serialize_task_tree(self, tasks):
        serializer = TaskSerializer(tasks, many=True)
        task_data = serializer.data
        
        # 为每个任务添加子任务
        for i, task in enumerate(tasks):
            children = task.children.all()
            if children.exists():
                task_data[i]['children'] = self._serialize_task_tree(children)
            else:
                task_data[i]['children'] = []
        
        return task_data