from django.urls import path
from . import views

urlpatterns = [
    path('log/', views.log_kana_result, name='kana_log'),
    path('next/', views.next_kana, name='kana_next'),
]
