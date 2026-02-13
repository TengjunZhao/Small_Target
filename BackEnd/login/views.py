from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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


# 2. 用户注册接口（无需登录即可访问）
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # 获取注册信息
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        # 验证必填字段
        if not username or not password:
            return Response({
                'code': 400,
                'msg': '用户名和密码不能为空',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查用户名是否已存在
        if User.objects.filter(username=username).exists():
            return Response({
                'code': 400,
                'msg': '用户名已存在',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 检查邮箱是否已存在（如果提供了邮箱）
        if email and User.objects.filter(email=email).exists():
            return Response({
                'code': 400,
                'msg': '邮箱已被注册',
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 创建用户
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email
            )
            
            # 生成 JWT Token
            refresh = RefreshToken.for_user(user)
            return Response({
                'code': 200,
                'msg': '注册成功',
                'data': {
                    'token': str(refresh.access_token),
                    'refresh': str(refresh),
                    'username': user.username,
                    'is_superuser': user.is_superuser
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'code': 500,
                'msg': f'注册失败: {str(e)}',
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 3. 用户信息接口（需登录才能访问）
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