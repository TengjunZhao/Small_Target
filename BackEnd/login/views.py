from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated


# 1. 登录接口（无需登录即可访问）
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 获取前端传的账号密码
        username = request.data.get('username')
        password = request.data.get('password')

        # 校验账号密码
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'code': 400,
                'msg': '账号或密码错误',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # 生成 JWT Token
        refresh = RefreshToken.for_user(user)
        return Response({
            'code': 200,
            'msg': '登录成功',
            'data': {
                'token': str(refresh.access_token),  # Access Token
                'refresh': str(refresh),  # Refresh Token（可选）
                'username': user.username,
                'is_superuser': user.is_superuser
            }
        }, status=status.HTTP_200_OK)


# 2. 用户信息接口（需登录才能访问）
class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 获取当前登录用户信息
        user = request.user
        return Response({
            'code': 200,
            'msg': '获取用户信息成功',
            'data': {
                'username': user.username,
                'email': user.email,
                'is_superuser': user.is_superuser,
                'is_staff': user.is_staff,
                'id':user.id
            }
        }, status=status.HTTP_200_OK)