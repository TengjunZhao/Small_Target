"""
URL configuration for Small_Target project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home_view(request):
    return JsonResponse({
        'message': 'Welcome to Small Target API',
        'api_endpoints': {
            'kana': '/api/kana/',
            'admin': '/admin/'
        },
        'status': 'success'
    })

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    # Expose Kana API under /api/kana/
    path('api/kana/', include('kana.urls')),
    # Project management API
    path('api/projects/', include('project_management.urls')),
]
