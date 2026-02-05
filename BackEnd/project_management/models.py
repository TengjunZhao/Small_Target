from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    """项目模型"""
    name = models.CharField(max_length=100, verbose_name='项目名称')
    description = models.TextField(blank=True, verbose_name='项目描述')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='项目负责人')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = '项目列表'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name

class Task(models.Model):
    """任务模型"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks', verbose_name='所属项目')
    name = models.CharField(max_length=100, verbose_name='任务名称')
    description = models.TextField(blank=True, verbose_name='任务描述')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(verbose_name='结束日期')
    duration = models.IntegerField(verbose_name='持续天数')
    progress = models.FloatField(default=0, verbose_name='完成进度')  # 0 to 100
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name='父任务')
    priority = models.IntegerField(choices=[(1, '低'), (2, '中'), (3, '高')], default=2, verbose_name='优先级')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '任务'
        verbose_name_plural = '任务列表'
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.project.name} - {self.name}"
    
    @property
    def is_completed(self):
        return self.progress >= 100
    
    @property
    def status(self):
        if self.progress >= 100:
            return '已完成'
        elif self.progress > 0:
            return '进行中'
        else:
            return '未开始'

class TaskDependency(models.Model):
    """任务依赖关系"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependencies', verbose_name='任务')
    depends_on = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='dependents', 
                                  verbose_name='依赖的任务')
    dependency_type = models.CharField(max_length=20, choices=[
        ('FS', '完成-开始'),
        ('SS', '开始-开始'),
        ('FF', '完成-完成'),
        ('SF', '开始-完成')
    ], default='FS', verbose_name='依赖类型')
    
    class Meta:
        verbose_name = '任务依赖'
        verbose_name_plural = '任务依赖关系'
        unique_together = ['task', 'depends_on']
    
    def __str__(self):
        return f"{self.depends_on.name} -> {self.task.name}"

# Demo数据创建函数
def create_demo_data():
    """创建演示数据"""
    from django.contrib.auth.models import User
    from datetime import date, timedelta
    
    # 创建用户
    user, created = User.objects.get_or_create(username='demo_user')
    if created:
        user.set_password('demo123')
        user.save()
    
    # 创建项目
    project, created = Project.objects.get_or_create(
        name='网站开发项目',
        defaults={
            'description': '开发一个企业官网系统',
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=60),
            'owner': user
        }
    )
    
    if created:
        # 创建主任务
        design_task = Task.objects.create(
            project=project,
            name='UI设计',
            description='完成网站整体UI设计',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=15),
            duration=15,
            progress=60,
            priority=3
        )
        
        frontend_task = Task.objects.create(
            project=project,
            name='前端开发',
            description='实现网站前端页面',
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=35),
            duration=25,
            progress=30,
            priority=3
        )
        
        backend_task = Task.objects.create(
            project=project,
            name='后端开发',
            description='开发网站后台API',
            start_date=date.today() + timedelta(days=15),
            end_date=date.today() + timedelta(days=45),
            duration=30,
            progress=10,
            priority=3
        )
        
        testing_task = Task.objects.create(
            project=project,
            name='系统测试',
            description='进行全面测试',
            start_date=date.today() + timedelta(days=40),
            end_date=date.today() + timedelta(days=55),
            duration=15,
            progress=0,
            priority=2
        )
        
        deploy_task = Task.objects.create(
            project=project,
            name='部署上线',
            description='部署到生产环境',
            start_date=date.today() + timedelta(days=55),
            end_date=date.today() + timedelta(days=60),
            duration=5,
            progress=0,
            priority=1
        )
        
        # 创建子任务
        homepage_design = Task.objects.create(
            project=project,
            name='首页设计',
            description='设计网站首页',
            start_date=date.today(),
            end_date=date.today() + timedelta(days=5),
            duration=5,
            progress=100,
            parent=design_task,
            priority=2
        )
        
        innerpage_design = Task.objects.create(
            project=project,
            name='内页设计',
            description='设计网站内页模板',
            start_date=date.today() + timedelta(days=5),
            end_date=date.today() + timedelta(days=15),
            duration=10,
            progress=40,
            parent=design_task,
            priority=2
        )
        
        # 创建依赖关系
        TaskDependency.objects.create(task=frontend_task, depends_on=design_task, dependency_type='FS')
        TaskDependency.objects.create(task=testing_task, depends_on=frontend_task, dependency_type='FS')
        TaskDependency.objects.create(task=testing_task, depends_on=backend_task, dependency_type='FS')
        TaskDependency.objects.create(task=deploy_task, depends_on=testing_task, dependency_type='FS')
    
    return project