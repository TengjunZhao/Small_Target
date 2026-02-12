from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='kana_index'),
    path('next/', views.GetNextKanaView.as_view(), name='kana_next'),
    path('log/', views.LogResultView.as_view(), name='kana_log'),
    path('errors/', views.GetErrorListView.as_view(), name='kana_errors'),
]