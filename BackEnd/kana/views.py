from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import json
import random
from django.db import transaction
from .models import Kana, UserProgress

def _weighted_choice(items, weights):
    """加权随机选择算法"""
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for item, w in zip(items, weights):
        upto += w
        if r <= upto:
            return item
    return items[0]

@csrf_exempt
def index(request):
    return JsonResponse({'message': 'Hello from kana app!'})

class GetNextKanaView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取下一个要练习的假名"""
        # 调试信息
        print(f"DEBUG: Authentication: {request.user}")
        print(f"DEBUG: Authenticated: {request.user.is_authenticated}")
        print(f"DEBUG: Authorization header: {request.META.get('HTTP_AUTHORIZATION', 'None')}")
        
        try:
            user_id = int(request.GET.get('user_id', 1))
            
            # 获取所有假名
            all_kana = list(Kana.objects.all())
            if not all_kana:
                return Response({'error': '没有可用的假名数据'}, status=status.HTTP_404_NOT_FOUND)
            
            # 随机选择一个假名
            current_kana = random.choice(all_kana)
            
            # 生成选项（包括正确答案和3个错误答案）
            options = [current_kana.romaji]
            other_kana = [k for k in all_kana if k.id != current_kana.id]
            
            # 添加3个随机错误选项
            if len(other_kana) >= 3:
                wrong_options = random.sample(other_kana, 3)
                options.extend([k.romaji for k in wrong_options])
            else:
                # 如果假名数量不足，添加一些常见选项
                common_romaji = ['a', 'i', 'u', 'e', 'o', 'ka', 'ki', 'ku', 'ke', 'ko']
                wrong_options = [r for r in common_romaji if r != current_kana.romaji][:3]
                options.extend(wrong_options)
            
            # 打乱选项顺序
            random.shuffle(options)
            
            return Response({
                'id': current_kana.id,
                'hira': current_kana.hiragana,
                'kata': current_kana.katakana,
                'romaji': current_kana.romaji,
                'options': options
            })
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LogResultView(APIView):
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        """记录练习结果"""
        try:
            data = request.data
            user_id = data.get('user_id', 1)
            kana_id = data.get('kana_id')  # 修改为kana_id
            correct = data.get('correct', False)
            
            if not kana_id:
                return Response({'error': '缺少kana_id参数'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 查找对应的假名 - 使用id确保唯一性
            try:
                kana = Kana.objects.get(id=kana_id)  # 使用get()确保唯一
            except Kana.DoesNotExist:
                return Response({'error': f'假名ID {kana_id} 不存在'}, status=status.HTTP_404_NOT_FOUND)
            
            # 获取或创建用户进度记录
            progress, created = UserProgress.objects.get_or_create(
                user_id=user_id,
                kana=kana,
                defaults={
                    'correct_count': 0,
                    'wrong_count': 0
                }
            )
            
            # 更新计数
            if correct:
                progress.correct_count += 1
            else:
                progress.wrong_count += 1
            
            progress.last_practiced = timezone.now()
            progress.save()
            
            # 添加调试信息
            print(f"DEBUG: log_result - user_id={user_id}, kana_id={kana_id}, romaji='{kana.romaji}', correct={correct}, created={created}, progress_id={progress.id}")
            
            return Response({
                'message': '记录成功',
                'progress': {
                    'correct_count': progress.correct_count,
                    'wrong_count': progress.wrong_count,
                    'accuracy_rate': progress.accuracy_rate
                }
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetErrorListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取用户的错误列表（高频错误）"""
        # 调试信息
        print(f"DEBUG ErrorList: Authentication: {request.user}")
        print(f"DEBUG ErrorList: Authenticated: {request.user.is_authenticated}")
        print(f"DEBUG ErrorList: Authorization header: {request.META.get('HTTP_AUTHORIZATION', 'None')}")
        
        try:
            user_id = int(request.GET.get('user_id', 1))
            limit = int(request.GET.get('limit', 10))
            
            # 获取错误次数较多的假名（错误次数大于正确次数）
            error_progress = UserProgress.objects.filter(
                user_id=user_id,
                wrong_count__gt=0
            ).order_by('-wrong_count')[:limit]
            
            error_list = []
            for progress in error_progress:
                error_list.append({
                    'hira': progress.kana.hiragana,
                    'kata': progress.kana.katakana,
                    'romaji': progress.kana.romaji,
                    'errors': progress.wrong_count,
                    'corrects': progress.correct_count,
                    'accuracy_rate': progress.accuracy_rate
                })
            
            return Response({
                'error_list': error_list,
                'total_errors': sum(p.wrong_count for p in error_progress)
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)