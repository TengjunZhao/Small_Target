from django.urls import path
from .views import LoginView, RegisterView, UserInfoView

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/info/', UserInfoView.as_view(), name='user_info'),
]