"""
URL configuration for budget project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path


from family.views import HomePageView, LoginUserView, UserListView, CategoryListView, CreateCategoryView, \
    IncomeListView, IncomeCreateView, ReportView, CreateReportView, ExpenseListView, ExpenseCreateView, AddUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name='home'),
    path('users/', UserListView.as_view(), name='users'),
    path('registration/', AddUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('category_list/', CategoryListView.as_view(), name='category_list'),
    path('create_category/', CreateCategoryView.as_view(), name='create_category'),
    path('income_list/', IncomeListView.as_view(), name='income_list'),
    path('create_income/', IncomeCreateView.as_view(), name='create_income'),
    path('expense_list/', ExpenseListView.as_view(), name='expense_list'),
    path('create_expense/', ExpenseCreateView.as_view(), name='create_expense'),
    path('create_report/', CreateReportView.as_view(), name='create_report'),
    path('report_list/', ReportView.as_view(), name='report_list'),

]

