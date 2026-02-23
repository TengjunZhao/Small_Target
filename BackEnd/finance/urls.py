from django.urls import path
from . import views

urlpatterns = [
    path('import-bill/', views.ImportBillView.as_view(), name='import_bill'),
    path('user-email-config/', views.UserEmailConfigView.as_view(), name='user_email_config'),
    path('pending-expense/', views.PendingExpenseListView.as_view(), name='pending_expense'),
    path('bill/', views.BillListView.as_view(), name='bill'),
    path('family-members/', views.FamilyMembersView.as_view(), name='family_members'),
    path('import-status/', views.ImportBillView.as_view(), name='import_status'),  # 获取导入状态
    path('income-types/', views.IncomeTypeView.as_view(), name='income_types'),
    path('incomes/', views.IncomeView.as_view(), name='incomes'),
    path('analysis/', views.FinanceAnalysisView.as_view(), name='finance_analysis'),
    path('budget-sub-category/', views.BudgetSubCategoryView.as_view(), name='budget_sub_category'),
]