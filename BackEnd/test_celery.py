import os
import django
from celery import current_app

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Small_Target.settings')
django.setup()

# 导入任务
from finance.tasks import import_bill_task

print("=== Celery 任务测试 ===")
print(f"Celery 应用: {current_app}")
print(f"Broker URL: {current_app.conf.broker_url}")
print(f"Result Backend: {current_app.conf.result_backend}")

# 测试任务
print("\n=== 发送测试任务 ===")
try:
    # 使用测试用户ID（假设为1）
    result = import_bill_task.delay(user_id=1, alipay_password='test', wechat_password='test')
    print(f"任务已发送，任务ID: {result.id}")
    print(f"任务状态: {result.state}")
    
    # 等待几秒钟查看结果
    import time
    time.sleep(3)
    
    print(f"任务状态更新: {result.state}")
    if result.ready():
        print(f"任务结果: {result.result}")
    else:
        print("任务仍在执行中...")
        
except Exception as e:
    print(f"任务执行出错: {e}")
    import traceback
    traceback.print_exc()