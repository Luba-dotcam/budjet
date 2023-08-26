from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from django.utils import timezone

from family.models import Category, Income, Report, Expense
from family.validators import validate_username


class AddUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, validators=[validate_username])

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'category', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class DateRangeForm(forms.Form):
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
    transaction_type = forms.ChoiceField(choices=[], widget=forms.HiddenInput, required=False)


class SelectableDateRangeForm(DateRangeForm):
    start_date = forms.DateField(
        widget=SelectDateWidget(years=range(timezone.now().year - 10, timezone.now().year + 1))
    )
    end_date = forms.DateField(
        widget=SelectDateWidget(years=range(timezone.now().year - 10, timezone.now().year + 1))
    )


class DateForm(forms.Form):
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }