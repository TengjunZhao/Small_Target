from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import random
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

@csrf_exempt
def get_next_kana(request):
    """获取下一个要练习的假名"""
    try:
        user_id = int(request.GET.get('user_id', 1))
        
        # 获取所有假名
        all_kana = list(Kana.objects.all())
        if not all_kana:
            return JsonResponse({'error': '没有可用的假名数据'}, status=404)
        
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
        
        return JsonResponse({
            'id': current_kana.id,
            'hira': current_kana.hiragana,
            'kata': current_kana.katakana,
            'romaji': current_kana.romaji,
            'options': options
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def log_result(request):
    """记录练习结果"""
    if request.method != 'POST':
        return JsonResponse({'error': '只支持POST方法'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id', 1)
        romaji = data.get('romaji')
        correct = data.get('correct', False)
        
        if not romaji:
            return JsonResponse({'error': '缺少romaji参数'}, status=400)
        
        # 查找对应的假名
        try:
            kana = Kana.objects.get(romaji=romaji)
        except Kana.DoesNotExist:
            return JsonResponse({'error': f'假名 {romaji} 不存在'}, status=404)
        
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
        
        return JsonResponse({
            'message': '记录成功',
            'progress': {
                'correct_count': progress.correct_count,
                'wrong_count': progress.wrong_count,
                'accuracy_rate': progress.accuracy_rate
            }
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': '无效的JSON数据'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def get_error_list(request):
    """获取用户的错误列表（高频错误）"""
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
        
        return JsonResponse({
            'error_list': error_list,
            'total_errors': sum(p.wrong_count for p in error_progress)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)