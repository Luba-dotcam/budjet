from django.utils import timezone
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
import pytest
from family.models import Category, Income, UserProfile


@pytest.mark.django_db
def test_home_page_view():
    url = reverse('home')
    client = Client()
    response = client.get(url)
    assert response.status_code == 200
    assert 'Welcome' in str(response.content)


@pytest.mark.django_db
def test_user_list_view(create_user):
    url = reverse('home')
    client = Client()
    client.force_login(create_user)
    response = client.get(url)
    assert response.status_code == 200
    assert 'Welcome, testuser!' in str(response.content)
    assert 'Welcome to Your Budget' in str(response.content)
    assert '<a href="/logout/">Logout</a>' in str(response.content)


@pytest.mark.django_db
def test_add_user_view():
    client = Client()
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    expected_content = 'Registration'
    assert expected_content in response.content.decode('utf-8')


@pytest.mark.django_db
def test_login_valid_user():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302
    assert response.url == reverse('home')
    assert response.wsgi_request.user.is_authenticated


@pytest.mark.django_db
def test_logout_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = Client()
    client.login(username='testuser', password='testpassword')
    url = reverse('logout')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/'
    assert response.wsgi_request.user.is_anonymous


@pytest.mark.django_db
def test_category_list_view():

    Category.objects.create(name='Category 1')
    Category.objects.create(name='Category 2')
    Category.objects.create(name='Category 3')

    client = Client()
    url = reverse('category_list')

    response = client.get(url)

    assert response.status_code == 200
    assert len(response.context['categories']) == 3
    assert b'Category 1' in response.content
    assert b'Category 2' in response.content
    assert b'Category 3' in response.content


@pytest.mark.django_db
def test_create_category_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    client = Client()
    client.login(username='testuser', password='testpassword')
    create_url = reverse('create_category')
    form_data = {
        'name': 'Test Category',
        'type': 'income',
    }
    initial_category_count = Category.objects.count()
    post_response = client.post(create_url, data=form_data, follow=True)
    assert post_response.status_code == 200
    assert Category.objects.count() == initial_category_count + 1
    assert post_response.redirect_chain[-1][0] == reverse('category_list')


@pytest.mark.django_db
def test_income_list_view():
    user = User.objects.create_user(username='testuser', password='testpassword')
    user_profile = UserProfile.objects.create(user=user)
    some_existing_category, created = Category.objects.get_or_create(name='Some Category', type='income')

    today = timezone.now().date()
    income1 = Income.objects.create(user=user_profile, amount=100, category=some_existing_category, date=today)
    client = Client()
    client.login(username='testuser', password='testpassword')
    income_list_url = reverse('income_list')
    get_response = client.get(income_list_url)
    assert get_response.status_code == 200
    assert 'incomes' in get_response.context
    incomes = get_response.context['incomes']
    assert income1 in incomes


@pytest.mark.django_db
def test_income_create_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    UserProfile.objects.create(user=user)
    client.login(username='testuser', password='testpassword')

    get_response = client.get(reverse('create_income'))
    assert get_response.status_code == 200

    post_data = {'amount': '100', 'date': '2023-08-23'}

    post_response = client.post(reverse('create_income'), data=post_data, follow=True)
    assert post_response.status_code == 200


@pytest.mark.django_db
def test_expense_list_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('expense_list'))
    assert response.status_code == 200

    assert 'expense_list.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_expense_create_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('create_expense'))
    assert response.status_code == 200

    post_data = {'amount': '50', 'date': '2023-08-23'}
    post_response = client.post(reverse('create_expense'), data=post_data, follow=True)
    assert post_response.status_code == 200

    assert 'expense_create.html' in [template.name for template in post_response.templates]


@pytest.mark.django_db
def test_create_report_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('create_report'))
    assert response.status_code == 200

    post_data = {'title': 'Test Report', 'content': 'This is a test report content.'}
    post_response = client.post(reverse('create_report'), data=post_data, follow=True)
    assert post_response.status_code == 200
    assert 'create_report.html' in [template.name for template in post_response.templates]


@pytest.mark.django_db
def test_report_view():
    client = Client()
    user = User.objects.create_user(username='testuser', password='testpassword')
    user_profile = UserProfile.objects.create(user=user)
    client.login(username='testuser', password='testpassword')

    response = client.get(reverse('report_list'))
    assert response.status_code == 200

    assert 'reports_list.html' in [template.name for template in response.templates]