import logging
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.forms.widgets import DateInput
from .forms import AddUserForm, LoginForm, CategoryForm, DateRangeForm, ReportForm, IncomeForm, ExpenseForm
from family.models import Category, UserProfile, Income, Expense


# View for the home page
class HomePageView(View):
    template_name = 'home.html'

    # Retrieve the user
    def get(self, request, *args, **kwargs):
        user = request.user
        return render(request, self.template_name, {'user': user})


logger = logging.getLogger(__name__)


# View for listing users
class UserListView(View):
    # Retrieve all users from the database
    def get(self, request):
        users = User.objects.all()
        return render(request, 'home.html', {'users': users})


# View for adding new users
class AddUserView(View):
    # Display a form for adding a new user
    def get(self, request):
        form = AddUserForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Check if the passwords match
            if form.cleaned_data['password1'] == form.cleaned_data['password2']:
                user.set_password(form.cleaned_data['password1'])
                user.save()
                # Create a user profile for the new user
                user_profile = UserProfile.objects.create(
                    user=user,
                    username=user.username,
                    email=form.cleaned_data['email']
                )
                # Log in the new user and redirect to the home page
                login(request, user)
                return redirect('home')

        return render(request, 'registration.html', {'form': form})


# View for user login
class LoginUserView(View):
    # Display the login form
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username =form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            url = request.GET.get('next', 'home')
            if user is not None:
                login(request, user)
            return redirect(url)
        return render(request, 'login.html', {'form': form})


# View for user logout
class LogoutView(View):
    # Log out the current user and redirect to the login page
    def get(self, request):
        logout(request)
        return redirect('login')


# View for listing categories
class CategoryListView(View):
    # Retrieve all categories from the database
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'category_list.html', {'categories': categories})


# View for creating a new category
class CreateCategoryView(View):
    template_name = 'create_category.html'

    def get(self, request):
        form = CategoryForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('category_list')

        return render(request, self.template_name, {'form': form})


# View for listing incomes
class IncomeListView(View):
    template_name = 'income_list.html'

    @method_decorator(login_required)
    def get(self, request):
        form = DateRangeForm(request.GET)
        user_profile = None

        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            pass

        incomes = Income.objects.filter(user=user_profile)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            incomes = incomes.filter(date__range=(start_date, end_date))

        return render(request, self.template_name, {'incomes': incomes, 'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user.userprofile
            income.save()
            return redirect('income_list')

        return render(request, self.template_name, {'form': form})


# View for creating a new income
class IncomeCreateView(View):
    template_name = 'income_create.html'

    def get(self, request):
        form = IncomeForm()
        form.fields['date'].widget = DateInput(attrs={'type': 'date'})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = IncomeForm(request.POST)

        if form.is_valid():
            income = form.save(commit=False)
            user_profile = request.user.userprofile

            if user_profile:
                income.user = user_profile
                income.save()
                return HttpResponseRedirect(reverse('income_list'))

            else:
                messages.error(request, "User profile not found. Please contact support.")
                return redirect('income_create')

        return render(request, self.template_name, {'form': form})


# View for listing expenses
class ExpenseListView(View):
    template_name = 'expense_list.html'

    @method_decorator(login_required)
    def get(self, request):
        form = DateRangeForm(request.GET)
        expenses = Expense.objects.filter(user=request.user.userprofile)

        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            expenses = expenses.filter(date__range=(start_date, end_date))

        return render(request, self.template_name, {'expenses': expenses, 'form': form})


# View for creating a new expense
class ExpenseCreateView(View):
    template_name = 'expense_create.html'

    def get(self, request):
        form = ExpenseForm()
        form.fields['date'].widget = DateInput(attrs={'type': 'date'})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            user_profile = request.user.userprofile

            if user_profile:
                expense.user = user_profile
                expense.save()
                return redirect('expense_list')
            else:
                messages.error(request, "User profile not found. Please contact support.")
                return redirect('expense_create')

        return render(request, self.template_name, {'form': form})


# View for generating and displaying reports
class ReportView(View):
    template_name = 'reports_list.html'

    def get(self, request):
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            total_income = Income.objects.filter(user=user_profile).aggregate(total_income=Sum('amount'))[
                               'total_income'] or 0
            total_expense = Expense.objects.filter(user=user_profile).aggregate(total_expense=Sum('amount'))[
                                'total_expense'] or 0
            context = {
                'total_income': total_income,
                'total_expense': total_expense,
            }
            return render(request, self.template_name, context)
        else:
            return render(request, self.template_name, {})


# View for creating a new report
class CreateReportView(View):
    template_name = 'create_report.html'

    @method_decorator(login_required)
    def get(self, request):
        form = ReportForm()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user.userprofile
            report.save()
            return redirect('report_list')

        return render(request, self.template_name, {'form': form})




