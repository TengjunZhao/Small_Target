import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import Kana, KanaProgress

User = get_user_model()

def _get_or_guest_user(user_id=None):
    if user_id:
        try:
            return User.objects.get(id=int(user_id))
        except User.DoesNotExist:
            pass
    user, created = User.objects.get_or_create(username='guest')
    if created:
        user.set_unusable_password()
        user.save()
    return user


@csrf_exempt
def log_kana_result(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body.decode())
        user_id = data.get('user_id')
        romaji = data.get('romaji')
        correct = bool(data.get('correct'))
    except Exception:
        return JsonResponse({'error': 'invalid payload'}, status=400)

    user = _get_or_guest_user(user_id)
    try:
        kana = Kana.objects.get(romaji=romaji)
    except Kana.DoesNotExist:
        return JsonResponse({'error': 'kana not found'}, status=404)

    pr, _ = KanaProgress.objects.get_or_create(user=user, kana=kana)
    if correct:
        current = pr.weight if pr.weight is not None else kana.base_weight
        pr.weight = max(1, current - 1)
    else:
        current = pr.weight if pr.weight is not None else kana.base_weight
        pr.weight = min(10, current + 2)
        pr.errors = pr.errors + 1
    pr.save()
    return JsonResponse({'ok': True, 'romaji': romaji, 'weight': pr.weight, 'errors': pr.errors})


def _weighted_choice(items, weights):
    import random
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for item, w in zip(items, weights):
        upto += w
        if r <= upto:
            return item
    return items[0]


def next_kana(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'GET required'}, status=405)
    user_id = request.GET.get('user_id')
    user = _get_or_guest_user(user_id)

    kana_list = list(Kana.objects.all())
    if not kana_list:
        return JsonResponse({'error': 'no kana seeded'}, status=500)

    weighted = []
    for k in kana_list:
        pr = KanaProgress.objects.filter(user=user, kana=k).first()
        w = pr.weight if pr and pr.weight is not None else k.base_weight
        weighted.append((k, w, pr.errors if pr else 0))

    kana = _weighted_choice([k for k, _, _ in weighted], [w for _, w, _ in weighted])
    pr = KanaProgress.objects.filter(user=user, kana=kana).first()
    weight = pr.weight if pr and pr.weight is not None else kana.base_weight
    errors = pr.errors if pr else 0

    wrong_romaji = list(Kana.objects.exclude(romaji=kana.romaji).values_list('romaji', flat=True))
    import random
    random.shuffle(wrong_romaji)
    options = [kana.romaji, *wrong_romaji[:2]]
    random.shuffle(options)

    return JsonResponse({
        'hira': kana.hira,
        'kata': kana.kata,
        'romaji': kana.romaji,
        'weight': weight,
        'errors': errors,
        'options': options,
    })
