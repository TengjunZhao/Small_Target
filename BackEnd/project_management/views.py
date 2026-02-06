from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project, Task, TaskDependency
from .serializers import ProjectSerializer, TaskSerializer, TaskDependencySerializer, ProjectDetailSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    """项目视图集"""
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return super().get_serializer_class()
    
    # @action(detail=False, methods=['post'])
    # def create_demo(self, request):
    #     """创建演示数据"""
    #     try:
    #         project = create_demo_data()
    #         serializer = self.get_serializer(project)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     except Exception as e:
    #         return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def gantt_data(self, request, pk=None):
        """获取甘特图数据"""
        project = self.get_object()
        tasks = project.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

class TaskViewSet(viewsets.ModelViewSet):
    """任务视图集"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return Task.objects.filter(project_id=project_id)
        return super().get_queryset()
    
    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        """更新任务进度"""
        task = self.get_object()
        progress = request.data.get('progress')
        
        if progress is not None:
            try:
                progress = float(progress)
                if 0 <= progress <= 100:
                    task.progress = progress
                    task.save()
                    serializer = self.get_serializer(task)
                    return Response(serializer.data)
                else:
                    return Response({'error': '进度必须在0-100之间'}, 
                                  status=status.HTTP_400_BAD_REQUEST)
            except (ValueError, TypeError):
                return Response({'error': '无效的进度值'}, 
                              status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': '缺少进度参数'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class TaskDependencyViewSet(viewsets.ModelViewSet):
    """任务依赖视图集"""
    queryset = TaskDependency.objects.all()
    serializer_class = TaskDependencySerializer