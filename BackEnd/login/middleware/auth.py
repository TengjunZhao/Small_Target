"""全局鉴权中间件：拦截未登录请求"""
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 1. 放行不需要鉴权的路径（登录接口、admin 后台）
        exempt_paths = [
            '/api/login/',          # 登录接口
            '/admin/',              # Django 后台
            '/api/token/refresh/',  # Token 刷新接口
        ]
        if any(request.path.startswith(path) for path in exempt_paths):
            response = self.get_response(request)
            return response

        # 2. 校验 Token
        try:
            # 从请求头获取 Token
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            print(f"DEBUG Middleware: Authorization header: {auth_header}")
            if not auth_header:
                print("DEBUG Middleware: No Authorization header found")
                raise KeyError('Authorization header missing')
            
            # 提取 Bearer token
            if not auth_header.startswith('Bearer '):
                raise KeyError('Invalid Authorization header format')
            
            token = auth_header.split(' ')[1]
            if not token:
                raise KeyError('Token is empty')
            
            # 验证 token
            jwt_auth = JWTAuthentication()
            validated_token = jwt_auth.get_validated_token(token)
            # 将用户信息绑定到 request
            user = jwt_auth.get_user(validated_token)
            request.user = user
        except (InvalidToken, TokenError, KeyError, AttributeError):
            # Token 无效/不存在，返回 401
            return JsonResponse({
                'code': 401,
                'msg': '登录态失效，请重新登录',
                'data': None
            }, status=401)

        # 3. 放行合法请求
        response = self.get_response(request)
        return response