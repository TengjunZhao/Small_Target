import os
import sys
from celery import Celery
from celery.utils.log import get_task_logger
import logging
from logging.handlers import RotatingFileHandler
import time
import datetime
from pathlib import Path

# ========== 第一步：先配置Django环境（必须优先） ==========
# 设置 Django 的设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Small_Target.settings')

# ========== 第二步：获取BASE_DIR（多平台自适应） ==========
# 优先从Django settings中获取BASE_DIR（更规范），兜底用手动计算
try:
    from django.conf import settings
    BASE_DIR = settings.BASE_DIR
except ImportError:
    BASE_DIR = Path(__file__).resolve().parent.parent

# 创建 Celery 应用实例
app = Celery('Small_Target')

# 从 Django 的设置文件中加载 Celery 配置
# namespace='CELERY' 意味着所有 Celery 相关的配置键都必须以 CELERY_ 开头
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 中发现任务
app.autodiscover_tasks()

# ========== 核心：配置Celery日志时区 + 多平台自适应路径 ==========
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

# ========== 关键修改：多平台自适应日志路径 ==========
# 定义日志路径（区分Windows/Linux）
if sys.platform == 'win32':  # Windows系统
    LOG_DIR = BASE_DIR / 'logs' / 'celery'  # 项目内路径：BackEnd/logs/celery
else:  # Linux/Mac系统
    LOG_DIR = Path('/var/log/celery')  # 保持原有系统路径

# 自动创建日志目录（避免FileNotFoundError）
LOG_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = LOG_DIR / 'worker.log'

# 配置Celery日志处理器
logger = get_task_logger('celery_task')  # 保留你设置的非保留名
# 清空原有处理器
logger.handlers = []
# 添加自定义时区的文件处理器（使用自适应路径）
handler = RotatingFileHandler(
    str(LOG_FILE),  # Path对象转字符串，兼容Windows路径分隔符
    maxBytes=10*1024*1024,
    backupCount=10,
    encoding='utf-8'
)

# 使用自定义的CST时区格式化器（保留你的原有配置）
formatter = CSTFormatter(
    '[%(asctime)s: %(levelname)s/%(processName)s] %(message)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 测试 Celery 工作是否正常（保留你的原有测试任务）
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')