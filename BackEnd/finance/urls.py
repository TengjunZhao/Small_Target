from django.urls import path
from . import views

urlpatterns = [
    path('import-bill/', views.ImportBillView.as_view(), name='import_bill'),
    path('user-email-config/', views.UserEmailConfigView.as_view(), name='user_email_config'),
]