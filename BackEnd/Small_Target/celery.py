import os
from celery import Celery
from celery.utils.log import get_task_logger
import logging
from logging.handlers import RotatingFileHandler
import time
import datetime


# 设置 Django 的设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Small_Target.settings')

# 创建 Celery 应用实例
app = Celery('Small_Target')

# 从 Django 的设置文件中加载 Celery 配置
# namespace='CELERY' 意味着所有 Celery 相关的配置键都必须以 CELERY_ 开头
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 中发现任务
app.autodiscover_tasks()

# ========== 核心：配置Celery日志时区 ==========
class CSTFormatter(logging.Formatter):
    """自定义日志格式化器，将UTC时间转为东八区"""
    def converter(self, timestamp):
        # 转换UTC时间为东八区
        dt = datetime.datetime.fromtimestamp(timestamp)
        dt = dt + datetime.timedelta(hours=8)
        return dt.timetuple()

    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt is None:
            datefmt = '%Y-%m-%d %H:%M:%S'
        return time.strftime(datefmt, dt)

# 配置Celery日志处理器
logger = get_task_logger('celery')
# 清空原有处理器
logger.handlers = []
# 添加自定义时区的文件处理器
handler = RotatingFileHandler(
    '/var/log/celery/worker.log',  # Celery日志路径，确保目录存在
    maxBytes=10*1024*1024,
    backupCount=10,
    encoding='utf-8'
)

# 使用自定义的CST时区格式化器
formatter = CSTFormatter(
    '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 测试 Celery 工作是否正常
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')