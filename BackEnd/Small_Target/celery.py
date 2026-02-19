import os
from celery import Celery

# 设置 Django 的设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Small_Target.settings')

# 创建 Celery 应用实例
app = Celery('small_target')

# 从 Django 的设置文件中加载 Celery 配置
# namespace='CELERY' 意味着所有 Celery 相关的配置键都必须以 CELERY_ 开头
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 中发现任务
app.autodiscover_tasks()

# 测试 Celery 工作是否正常
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')