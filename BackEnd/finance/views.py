import email
import os
import csv
import chardet
from charset_normalizer import detect
from zipfile import ZipFile
import pandas as pd
import imaplib
import email.header
import datetime
from datetime import datetime as dt
import requests
from bs4 import BeautifulSoup
import requests.utils
import shutil
import subprocess
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import UserProfile, Family, ExpendAlipay, ExpendWechat, ExpendMerged, BudgetCategory
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)

# 导入 Celery 任务
from .tasks import import_bill_task

# 账单导入API视图
class ImportBillView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # 获取请求参数
            wechat_password = request.data.get('wechat_password', '')
            alipay_password = request.data.get('alipay_password', '')
            
            if not wechat_password and not alipay_password:
                return Response({
                    'code': 400,
                    'msg': '请至少提供一个账单密码',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 异步启动 Celery 任务
            print("DEBUG: ImportBillView POST method called")
            task = import_bill_task.delay(
                user_id=request.user.id,
                alipay_password=alipay_password,
                wechat_password=wechat_password
            )
            
            return Response({
                'code': 200,
                'msg': '账单导入任务已启动',
                'data': {
                    'task_id': task.id,
                    'status': 'PENDING',
                    'progress': 0,
                    'message': '任务已提交到队列，正在等待处理...'
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"账单导入任务创建失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'任务创建失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def get(self, request):
        """获取任务状态"""
        task_id = request.GET.get('task_id')
        if not task_id:
            return Response({
                'code': 400,
                'msg': '缺少任务ID参数',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 获取任务状态
            task = import_bill_task.AsyncResult(task_id)
            
            # 使用 Celery 状态
            status_map = {
                'PENDING': 'pending',
                'STARTED': 'processing',
                'PROGRESS': 'processing',
                'SUCCESS': 'completed',
                'FAILURE': 'failed',
                'REVOKED': 'failed'
            }
            
            # 尝试获取任务状态，处理 DisabledBackend 异常
            try:
                task_state = task.state
                progress_info = task.info if hasattr(task, 'info') else {}
            except Exception as e:
                # 如果结果后端被禁用，返回默认状态
                logger.warning(f"结果后端不可用: {str(e)}")
                task_state = 'PENDING'
                progress_info = {}
            
            status_data = {
                'task_id': task_id,
                'status': status_map.get(task_state, 'pending'),
                'progress': progress_info.get('progress', 0) if isinstance(progress_info, dict) else 0,
                'message': progress_info.get('message', f'任务状态: {task_state}') if isinstance(progress_info, dict) else f'任务状态: {task_state}',
                'result': progress_info.get('result', None) if isinstance(progress_info, dict) else None,
                'created_at': None,
                'updated_at': None
            }
            
            return Response({
                'code': 200,
                'msg': '获取任务状态成功',
                'data': status_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取任务状态失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取任务状态失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 待确认支出明细API视图
class PendingExpenseListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print("PendingExpenseListView GET method called")  # 调试信息
        print(f"Request user authenticated: {request.user.is_authenticated}")
        print(f"Request user: {request.user}")
        print(f"Request user id: {getattr(request.user, 'id', 'No ID')}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request META: {dict(request.META)}")
        """获取待确认支出明细（belonging字段为空的记录）"""
        try:
            # 获取分页参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            offset = (page - 1) * page_size
            
            # 获取当前用户的家庭信息
            user = request.user
            print(f"DEBUG: Current user: {user.username if user.is_authenticated else 'Anonymous'}")
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
                print(f"DEBUG: User profile family: {family.family_name if family else 'None'}")
            except UserProfile.DoesNotExist:
                print("DEBUG: UserProfile.DoesNotExist")
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 查询belonging字段为空的记录，按trade_time倒序排列
            queryset = ExpendMerged.objects.filter(
                family=family,
                belonging__isnull=True
            ).select_related('budget').order_by('-trade_time')
            
            # 获取总数
            total_count = queryset.count()
            
            # 分页查询
            records = queryset[offset:offset + page_size]
            
            # 获取所有预算子分类选项
            budget_sub_categories = list(BudgetCategory.objects.filter(
                family=family
            ).values_list('sub_category', flat=True).distinct())
            
            # 序列化数据
            data_list = []
            for record in records:
                data_list.append({
                    'transaction_id': record.transaction_id,
                    'time': record.trade_time.strftime('%Y-%m-%d %H:%M:%S') if record.trade_time else '',
                    'amount': float(record.price) if record.price else 0,
                    'in_out': record.in_out or '',
                    'commodity': record.commodity or '',
                    'main_category': record.budget.main_category if record.budget else '',
                    'sub_category': record.budget.sub_category if record.budget else '',
                    'belonging': record.belonging or '',
                    'person': record.person or '',
                    'expend_channel': record.get_expend_channel_display() or record.expend_channel
                })
            
            return Response({
                'code': 200,
                'msg': '获取待确认支出明细成功',
                'data': {
                    'records': data_list,
                    'budget_sub_categories': budget_sub_categories,
                    'total': total_count,
                    'page': page,
                    'page_size': page_size,
                    'total_pages': (total_count + page_size - 1) // page_size
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取待确认支出明细失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取待确认支出明细失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """确认支出记录（更新belonging字段）"""
        try:
            record_id = request.data.get('transaction_id')
            category = request.data.get('category')
            belonging = request.data.get('belonging')  # 默认归属为户主
            adjusted_sub_category = request.data.get('adjusted_sub_category', '')
            print(f"DEBUG: Record ID: {record_id}, {category} ,{belonging}, {adjusted_sub_category}")
            if not record_id:
                return Response({
                    'code': 400,
                    'msg': '记录ID不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 查找记录
            try:
                record = ExpendMerged.objects.get(transaction_id=record_id)
            except ExpendMerged.DoesNotExist:
                return Response({
                    'code': 404,
                    'msg': '记录不存在',
                    'data': None
                }, status=status.HTTP_404_NOT_FOUND)
            
            # 更新记录
            record.belonging = belonging
            if belonging:
                record.status = belonging
            record.save()
            
            # 如果提供了调整的子分类，查找对应的预算分类
            if adjusted_sub_category:
                try:
                    # 根据调整的子分类查找budget_category
                    budget_category = BudgetCategory.objects.get(
                        family=record.family,
                        sub_category=adjusted_sub_category
                    )
                    record.budget = budget_category
                    record.save()
                    logger.info(f"更新预算分类成功: {budget_category.main_category} - {budget_category.sub_category}")
                except BudgetCategory.DoesNotExist:
                    # 如果找不到对应的预算分类，创建一个新的
                    if category:
                        budget_category, created = BudgetCategory.objects.get_or_create(
                            family=record.family,
                            main_category=category,
                            defaults={'sub_category': adjusted_sub_category, 'is_fixed': False}
                        )
                        record.budget = budget_category
                        record.save()
                        logger.info(f"创建新的预算分类: {budget_category.main_category} - {budget_category.sub_category}")
                    else:
                        logger.warning("未提供主分类，无法创建预算分类")
                except Exception as e:
                    logger.error(f"更新预算分类失败: {str(e)}")
            # 如果只提供了主分类但没有调整子分类
            elif category and not record.budget:
                try:
                    budget_category, created = BudgetCategory.objects.get_or_create(
                        family=record.family,
                        main_category=category,
                        defaults={'sub_category': '默认', 'is_fixed': False}
                    )
                    record.budget = budget_category
                    record.save()
                except Exception as e:
                    logger.warning(f"更新预算分类失败: {str(e)}")
            
            return Response({
                'code': 200,
                'msg': '支出记录确认成功',
                'data': {
                    'transaction_id': record.transaction_id,
                    'belonging': record.belonging
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"确认支出记录失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'确认支出记录失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 家庭成员列表API视图
class FamilyMembersView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取当前用户所属家庭的所有成员"""
        try:
            user = request.user
            print(f"获取家庭成员列表，当前用户: {user.username}")
            
            # 获取当前用户的家庭信息
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
                print(f"用户家庭: {family.family_name if family else 'None'}")
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if not family:
                return Response({
                    'code': 400,
                    'msg': '用户未分配到任何家庭',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取同一家庭的所有用户
            family_members = UserProfile.objects.filter(family=family).select_related('user')
            
            # 构造返回数据
            members_list = []
            for member_profile in family_members:
                members_list.append({
                    'user_id': member_profile.user.id,
                    'username': member_profile.user.username,
                    'is_admin': member_profile.is_admin,
                    'mobile': member_profile.mobile
                })
            
            print(f"找到 {len(members_list)} 个家庭成员")
            
            return Response({
                'code': 200,
                'msg': '获取家庭成员成功',
                'data': members_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取家庭成员列表失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取家庭成员失败: {str(e)}',
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 用户邮箱配置API视图
class UserEmailConfigView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # 获取用户邮箱配置
        try:
            user = request.user
            email = user.email or ''
            
            return Response({
                'code': 200,
                'msg': '获取邮箱配置成功',
                'data': {
                    'email': email,
                    'configured': bool(email)
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"获取邮箱配置失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取邮箱配置失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        # 设置用户邮箱配置
        try:
            email = request.data.get('email')
            email_password = request.data.get('email_password', '')
            
            if not email:
                return Response({
                    'code': 400,
                    'msg': '邮箱不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = request.user
            
            # 更新Django内置User模型的email字段
            user.email = email
            user.save()
            
            # 注意：出于安全考虑，邮箱密码不应该明文存储
            # 如果需要存储邮箱密码，应该使用加密方式存储
            # 这里暂时不处理邮箱密码存储
            
            return Response({
                'code': 200,
                'msg': '邮箱配置保存成功',
                'data': {
                    'email': email,
                    'configured': True
                }
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"保存邮箱配置失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'保存邮箱配置失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 收支明细API视图
class BillListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print("BillListView GET method called")  # 调试信息
        print(f"Request user authenticated: {request.user.is_authenticated}")
        print(f"Request user: {request.user}")
        print(f"Request user id: {getattr(request.user, 'id', 'No ID')}")
        try:
            # 获取当前用户的家庭信息
            user = request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)

            # 1. 获取前端传入的参数（带默认值，避免KeyError）
            try:
                page = int(request.GET.get('page', 1))
                page_size = int(request.GET.get('page_size', 10))
                print(f"分页参数: page={page}, page_size={page_size}")
            except (ValueError, TypeError) as e:
                logger.error(f"分页参数转换错误: {str(e)}, GET参数: {dict(request.GET)}")
                return Response({
                    'code': 400,
                    'msg': '分页参数格式错误',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)
            print(page, page_size)
            user_id = request.GET.get('user_id', '')  # 用户ID筛选
            category_id = request.GET.get('category_id', '')  # 分类ID筛选
            start_date = request.GET.get('startDate', '')
            end_date = request.GET.get('endDate', '')
            print(user_id, category_id, start_date, end_date)
            # 2. 初始化查询集（基础查询：当前家庭的所有支出记录）
            queryset = ExpendMerged.objects.filter(family=family)
            print(f"初始查询集数量: {queryset.count()}")
            
            # 3. 条件过滤：只在参数有值时才添加过滤条件
            # 过滤用户（如果传了user_id）
            if user_id and user_id.strip():
                queryset = queryset.filter(user_id=user_id)

            # 过滤分类（如果传了category_id）
            if category_id and category_id.strip():
                queryset = queryset.filter(budget_id=category_id)

            # 过滤时间范围（开始时间）
            if start_date and start_date.strip():
                try:
                    # 解析前端传入的日期字符串（格式：YYYY-MM-DD）
                    start_datetime = dt.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(trade_time__gte=start_datetime)
                except ValueError:
                    return Response({
                        'code': 400,
                        'msg': '开始日期格式错误，请使用YYYY-MM-DD格式',
                        'data': {}
                    })

            # 过滤时间范围（结束时间）
            if end_date and end_date.strip():
                try:
                    end_datetime = dt.strptime(end_date, '%Y-%m-%d')
                    # 结束时间加一天，确保包含当天所有记录
                    end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
                    queryset = queryset.filter(trade_time__lte=end_datetime)
                except ValueError:
                    return Response({
                        'code': 400,
                        'msg': '结束日期格式错误，请使用YYYY-MM-DD格式',
                        'data': {}
                    })

            # 4. 分页处理
            total = queryset.count()  # 总记录数
            # 计算偏移量（page从1开始）
            offset = (page - 1) * page_size
            # 分页查询
            records = queryset.order_by('-trade_time')[offset:offset + page_size]

            # 5. 序列化数据
            data_list = []
            for record in records:
                data_list.append({
                    'transaction_id': record.transaction_id,
                    'time': record.trade_time.strftime('%Y-%m-%d %H:%M:%S') if record.trade_time else '',
                    'amount': float(record.price) if record.price else 0,
                    'in_out': record.in_out,
                    'merchant': record.person or '',
                    'commodity': record.commodity or '',
                    'category': record.budget.sub_category if record.budget else '',
                    'user': record.user.username if record.user else '',
                    'remark': record.status or '',
                    'belonging': record.belonging or ''
                })

            # 6. 获取预算分类列表（包含ID和子分类名称）
            budget_categories = list(BudgetCategory.objects.filter(
                family=family
            ).values('id', 'sub_category').distinct())

            # 7. 构造返回数据（匹配前端预期格式）
            return Response({
                'code': 200,
                'msg': '查询成功',
                'data': {
                    'records': data_list,
                    'page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': (total + page_size - 1) // page_size,  # 总页数
                    'budget_categories': budget_categories
                }
            })

        except Exception as e:
            logger.error(f"查询收支明细失败: {str(e)}")
            # 异常捕获，返回友好提示
            return Response({
                'code': 500,
                'msg': f'查询失败：{str(e)}',
                'data': {}
            })