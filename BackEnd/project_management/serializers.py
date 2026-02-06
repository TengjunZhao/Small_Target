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
        
        # 构建父子关系映射
        task_map = {task['id']: task for task in task_data}
        children_map = {}
        
        # 构建子任务映射关系
        for task in task_data:
            task['children'] = []
            parent_id = task['parent_id']
            if parent_id:
                if parent_id not in children_map:
                    children_map[parent_id] = []
                children_map[parent_id].append(task)
        
        # 递归构建完整的树形结构
        def build_tree_recursive(task_item):
            task_id = task_item['id']
            if task_id in children_map:
                # 为当前任务添加子任务
                for child_task in children_map[task_id]:
                    # 递归构建子任务的子树
                    build_tree_recursive(child_task)
                    task_item['children'].append(child_task)
            return task_item
        
        # 只返回根任务（没有父任务的任务）
        root_tasks = [task for task in task_data if not task['parent_id']]
        
        # 为每个根任务构建完整的子树
        for root_task in root_tasks:
            build_tree_recursive(root_task)
        
        return root_tasks