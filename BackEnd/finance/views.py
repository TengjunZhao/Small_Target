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
from .models import UserProfile, Family, ExpendAlipay, ExpendWechat, ExpendMerged, BudgetCategory, Income, IncomeType, Asset
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
            return self._bad_request_response('缺少任务ID参数')
        
        try:
            # 获取任务状态
            task = import_bill_task.AsyncResult(task_id)
            
            # 提取任务状态信息
            task_info = self._extract_task_info(task)
            
            # 构建响应数据
            status_data = self._build_status_response(task_id, task_info)
            
            logger.info(f"任务状态获取成功: {status_data}")
            return Response({
                'code': 200,
                'msg': '获取任务状态成功',
                'data': status_data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取任务状态失败: {str(e)}", exc_info=True)
            return self._error_response(f'获取任务状态失败: {str(e)}')

    def _bad_request_response(self, message):
        """构建400错误响应"""
        return Response({
            'code': 400,
            'msg': message,
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def _error_response(self, message):
        """构建500错误响应"""
        return Response({
            'code': 500,
            'msg': message,
            'data': None
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _extract_task_info(self, task):
        """提取任务状态和详细信息"""
        status_map = {
            'PENDING': 'pending',
            'STARTED': 'processing',
            'PROGRESS': 'processing',
            'SUCCESS': 'completed',
            'FAILURE': 'failed',
            'REVOKED': 'failed'
        }
        
        try:
            task_state = task.state
            logger.info(f"任务状态: {task_state}")
            
            # 获取任务元数据
            progress_info = self._get_task_metadata(task, task_state)
            
            return {
                'state': task_state,
                'status': status_map.get(task_state, 'pending'),
                'info': progress_info
            }
            
        except Exception as e:
            logger.warning(f"获取任务详细信息失败: {str(e)}")
            # 即使出错也要返回基本信息
            fallback_state = getattr(task, 'state', 'PENDING') if hasattr(task, 'state') else 'PENDING'
            return {
                'state': fallback_state,
                'status': status_map.get(fallback_state, 'pending'),
                'info': {
                    'message': f'无法获取详细状态信息: {str(e)}',
                    'progress': 0
                }
            }
    
    def _get_task_metadata(self, task, task_state):
        """获取任务的元数据信息"""
        progress_info = {}
        
        # 获取通过 update_state 设置的元数据
        if hasattr(task, 'info') and task.info:
            progress_info = task.info if isinstance(task.info, dict) else {}
            logger.info(f"获取到的任务info: {progress_info}")
        else:
            logger.info("未获取到任务info")
        
        # FAILURE 状态下获取异常信息
        if task_state == 'FAILURE':
            self._extract_failure_info(task, progress_info)
            
        return progress_info
    
    def _extract_failure_info(self, task, progress_info):
        """提取失败任务的详细信息"""
        try:
            # 获取异常traceback
            exception_info = getattr(task, 'traceback', None)
            if exception_info:
                progress_info['exception_traceback'] = exception_info
                logger.info("获取到异常traceback信息")
                
            # 获取异常类型和消息（如果有的话）
            if hasattr(task, 'result') and isinstance(getattr(task, 'result', None), Exception):
                exc = task.result
                progress_info['exc_type'] = type(exc).__name__
                progress_info['exc_message'] = str(exc)
                
        except Exception as trace_error:
            logger.warning(f"获取failure信息失败: {trace_error}")
    
    def _build_status_response(self, task_id, task_info):
        """构建状态响应数据"""
        progress_info = task_info['info']
        
        status_data = {
            'task_id': task_id,
            'status': task_info['status'],
            'progress': progress_info.get('progress', 0),
            'message': self._get_status_message(progress_info, task_info['state']),
            'result': progress_info.get('result'),
            'exception_type': progress_info.get('exc_type'),
            'exception_message': progress_info.get('exc_message'),
            'created_at': None,
            'updated_at': None
        }
        
        # 优先显示详细的异常信息
        if status_data['exception_message']:
            status_data['message'] = status_data['exception_message']
            
        return status_data
    
    def _get_status_message(self, progress_info, task_state):
        """获取状态消息"""
        # 优先使用progress_info中的消息
        if progress_info.get('message'):
            return progress_info['message']
        # 否则使用默认状态消息
        return f'任务状态: {task_state}'
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

# 收入类型管理API视图
class IncomeTypeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取收入类型列表"""
        try:
            user = request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取收入类型列表
            income_types = IncomeType.objects.filter(family=family)
            
            data_list = []
            for income_type in income_types:
                data_list.append({
                    'id': income_type.id,
                    'income_maintype': income_type.income_maintype,
                    'income_subtype': income_type.income_subtype,
                    'create_time': income_type.create_time.strftime('%Y-%m-%d %H:%M:%S') if income_type.create_time else ''
                })
            
            return Response({
                'code': 200,
                'msg': '获取收入类型成功',
                'data': data_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取收入类型失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取收入类型失败: {str(e)}',
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """创建收入类型"""
        try:
            user = request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            income_maintype = request.data.get('income_maintype')
            income_subtype = request.data.get('income_subtype')
            
            if not income_maintype or not income_subtype:
                return Response({
                    'code': 400,
                    'msg': '收入类型和子类不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建收入类型
            income_type = IncomeType.objects.create(
                family=family,
                income_maintype=income_maintype,
                income_subtype=income_subtype
            )
            
            return Response({
                'code': 200,
                'msg': '收入类型创建成功',
                'data': {
                    'id': income_type.id,
                    'income_maintype': income_type.income_maintype,
                    'income_subtype': income_type.income_subtype
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"创建收入类型失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'创建收入类型失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 收入管理API视图
class IncomeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取收入记录列表"""
        try:
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
            
            # 获取分页参数
            page = int(request.GET.get('page', 1))
            page_size = int(request.GET.get('page_size', 10))
            offset = (page - 1) * page_size
            
            # 获取筛选参数
            user_id = request.GET.get('user_id', '')
            income_type_id = request.GET.get('income_type_id', '')
            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            
            # 基础查询
            queryset = Income.objects.filter(family=family)
            
            # 用户筛选
            if user_id and user_id.strip():
                queryset = queryset.filter(user_id=user_id)
            
            # 收入类型筛选
            if income_type_id and income_type_id.strip():
                queryset = queryset.filter(income_type_id=income_type_id)
            
            # 时间范围筛选
            if start_date and start_date.strip():
                try:
                    start_datetime = dt.strptime(start_date, '%Y-%m-%d')
                    queryset = queryset.filter(payday__gte=start_datetime)
                except ValueError:
                    return Response({
                        'code': 400,
                        'msg': '开始日期格式错误',
                        'data': {}
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            if end_date and end_date.strip():
                try:
                    end_datetime = dt.strptime(end_date, '%Y-%m-%d')
                    end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
                    queryset = queryset.filter(payday__lte=end_datetime)
                except ValueError:
                    return Response({
                        'code': 400,
                        'msg': '结束日期格式错误',
                        'data': {}
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取总数和分页数据
            total = queryset.count()
            records = queryset.order_by('-payday')[offset:offset + page_size]
            
            # 序列化数据
            data_list = []
            for record in records:
                data_list.append({
                    'id': record.id,
                    'amount': float(record.amount) if record.amount else 0,
                    'insurance': float(record.insurance) if record.insurance else 0,
                    'adjustment': float(record.adjustment) if record.adjustment else 0,
                    'income': float(record.income) if record.income else 0,
                    'payday': record.payday.strftime('%Y-%m-%d') if record.payday else '',
                    'income_type_maintype': record.income_type.income_maintype if record.income_type else '',
                    'income_type_subtype': record.income_type.income_subtype if record.income_type else '',
                    'user': record.user.username if record.user else '',
                    'remark': record.remark or '',
                    'create_time': record.create_time.strftime('%Y-%m-%d %H:%M:%S') if record.create_time else ''
                })
            
            # 获取收入类型选项
            income_types = list(IncomeType.objects.filter(family=family).values('id', 'income_maintype', 'income_subtype'))
            
            return Response({
                'code': 200,
                'msg': '获取收入记录成功',
                'data': {
                    'records': data_list,
                    'page': page,
                    'page_size': page_size,
                    'total': total,
                    'total_pages': (total + page_size - 1) // page_size,
                    'income_types': income_types
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取收入记录失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取收入记录失败: {str(e)}',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """创建收入记录"""
        try:
            user = request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取请求数据
            income_type_id = request.data.get('income_type_id')
            amount = request.data.get('amount')
            insurance = request.data.get('insurance', 0)
            adjustment = request.data.get('adjustment', 0)
            income = request.data.get('income')
            payday = request.data.get('payday')
            user_id = request.data.get('user_id')
            remark = request.data.get('remark', '')
            
            # 验证必填字段
            if not income_type_id or not amount or not payday or not income:
                return Response({
                    'code': 400,
                    'msg': '收入类型、税前总额、到账日期和税后收入不能为空',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 处理日期格式
            try:
                from datetime import datetime
                if isinstance(payday, str):
                    payday = datetime.strptime(payday, '%Y-%m-%d').date()
            except ValueError as e:
                return Response({
                    'code': 400,
                    'msg': f'日期格式错误，请使用 YYYY-MM-DD 格式: {str(e)}',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证收入类型是否存在
            try:
                income_type = IncomeType.objects.get(id=income_type_id, family=family)
            except IncomeType.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '收入类型不存在',
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 验证用户是否存在
            target_user = None
            if user_id:
                try:
                    target_user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    return Response({
                        'code': 400,
                        'msg': '指定的用户不存在',
                        'data': None
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建收入记录
            income_record = Income.objects.create(
                family=family,
                user=target_user,
                income_type=income_type,
                amount=amount,
                insurance=insurance,
                adjustment=adjustment,
                income=income,
                payday=payday,
                remark=remark
            )
            
            return Response({
                'code': 200,
                'msg': '收入记录创建成功',
                'data': {
                    'id': income_record.id,
                    'amount': float(income_record.amount),
                    'income': float(income_record.income),
                    'payday': income_record.payday.strftime('%Y-%m-%d') if income_record.payday else '',
                    'income_type': f"{income_type.income_maintype}-{income_type.income_subtype}",
                    'user': income_record.user.username if income_record.user else ''
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"创建收入记录失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'创建收入记录失败: {str(e)}',
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

# 预算分类子类目API视图
class BudgetSubCategoryView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取预算分类的子类目列表"""
        try:
            user = request.user
            try:
                user_profile = UserProfile.objects.get(user=user)
                family = user_profile.family
            except UserProfile.DoesNotExist:
                return Response({
                    'code': 400,
                    'msg': '用户未配置家庭信息',
                    'data': []
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 获取该家庭的所有预算分类
            budget_categories = BudgetCategory.objects.filter(family=family)
            
            # 构造返回数据
            categories_list = []
            for category in budget_categories:
                categories_list.append({
                    'id': category.id,
                    'main_category': category.main_category,
                    'sub_category': category.sub_category,
                    'is_fixed': category.is_fixed
                })
            
            return Response({
                'code': 200,
                'msg': '获取预算分类成功',
                'data': categories_list
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取预算分类失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取预算分类失败: {str(e)}',
                'data': []
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 财务分析API视图
class FinanceAnalysisView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取财务分析数据"""
        try:
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
            
            # 获取查询参数
            start_date = request.GET.get('start_date', '')
            end_date = request.GET.get('end_date', '')
            mode = request.GET.get('mode', 'family')  # 'family' 或 'personal'
            user_id = request.GET.get('user_id', '')
            
            # 验证必需参数
            if not start_date or not end_date:
                return Response({
                    'code': 400,
                    'msg': '请提供开始和结束日期',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 解析日期
            try:
                start_datetime = dt.strptime(start_date, '%Y-%m-%d')
                end_datetime = dt.strptime(end_date, '%Y-%m-%d')
                end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
            except ValueError:
                return Response({
                    'code': 400,
                    'msg': '日期格式错误，请使用YYYY-MM-DD格式',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 构建基础查询条件
            income_filter = {'family': family, 'payday__range': [start_datetime, end_datetime]}
            expense_filter = {'family': family, 'trade_time__range': [start_datetime, end_datetime]}
            
            # 根据模式添加用户筛选
            if mode == 'personal' and user_id:
                try:
                    target_user = User.objects.get(id=user_id)
                    income_filter['user'] = target_user
                    expense_filter['user'] = target_user
                except User.DoesNotExist:
                    return Response({
                        'code': 400,
                        'msg': '指定的用户不存在',
                        'data': {}
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # 查询收入数据
            incomes = Income.objects.filter(**income_filter)
            total_income = sum(float(income.income) for income in incomes)
            
            # 查询支出数据
            expenses = ExpendMerged.objects.filter(**expense_filter)
            total_expense = sum(float(expense.price) for expense in expenses if expense.in_out == '支出')
            
            # 计算结余和比例
            balance = total_income - total_expense
            income_ratio = (total_expense / total_income * 100) if total_income > 0 else 0
            
            # 支出分类统计
            expense_by_category = {}
            for expense in expenses:
                if expense.in_out == '支出':
                    category = expense.budget.sub_category if expense.budget else '未分类'
                    expense_by_category[category] = expense_by_category.get(category, 0) + float(expense.price)
            
            # 收入分类统计
            income_by_category = {}
            for income in incomes:
                category = f"{income.income_type.income_maintype}-{income.income_type.income_subtype}" if income.income_type else '未分类'
                income_by_category[category] = income_by_category.get(category, 0) + float(income.income)
            
            # 月度趋势数据（简化版：按月统计）
            monthly_trend = []
            current_month = start_datetime.replace(day=1)
            while current_month <= end_datetime:
                next_month = (current_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
                month_end = next_month - datetime.timedelta(days=1)
                
                # 统计该月的收入和支出
                month_income_filter = income_filter.copy()
                month_income_filter['payday__range'] = [current_month, min(month_end, end_datetime)]
                month_expense_filter = expense_filter.copy()
                month_expense_filter['trade_time__range'] = [current_month, min(month_end, end_datetime)]
                
                month_income = sum(float(income.income) for income in Income.objects.filter(**month_income_filter))
                month_expense = sum(float(expense.price) for expense in ExpendMerged.objects.filter(**month_expense_filter) if expense.in_out == '支出')
                
                monthly_trend.append({
                    'month': current_month.strftime('%Y-%m'),
                    'income': month_income,
                    'expense': month_expense
                })
                
                current_month = next_month
            
            # 构造返回数据
            data = {
                'total_income': round(total_income, 2),
                'total_expense': round(total_expense, 2),
                'balance': round(balance, 2),
                'income_ratio': round(income_ratio, 1),
                'expense_by_category': [
                    {'category': category, 'amount': round(amount, 2)}
                    for category, amount in expense_by_category.items()
                ],
                'income_by_category': [
                    {'category': category, 'amount': round(amount, 2)}
                    for category, amount in income_by_category.items()
                ],
                'monthly_trend': monthly_trend
            }
            
            return Response({
                'code': 200,
                'msg': '获取分析数据成功',
                'data': data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"获取财务分析数据失败: {str(e)}")
            return Response({
                'code': 500,
                'msg': f'获取分析数据失败: {str(e)}',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)