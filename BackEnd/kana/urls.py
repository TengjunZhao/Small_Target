from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='kana_index'),
    path('next/', views.get_next_kana, name='kana_next'),
    path('log/', views.log_result, name='kana_log'),
    path('errors/', views.get_error_list, name='kana_errors'),
]