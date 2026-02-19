@echo off
REM Celery Worker 启动脚本 (Windows)

REM 激活虚拟环境
call .venv\Scripts\activate.bat

REM 启动 Celery worker
 celery -A Small_Target worker --loglevel=info --pool=solo

pause