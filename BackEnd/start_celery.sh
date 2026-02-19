#!/bin/bash
# Celery Worker 启动脚本

# 激活虚拟环境
source .venv/bin/activate

# 启动 Celery worker
celery -A Small_Target worker --loglevel=info --pool=solo