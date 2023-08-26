import pytest
from django.contrib.auth.models import User
from family.models import Category
from django.test import Client


@pytest.fixture
def users():
    return [User.objects.create(username='user1'), User.objects.create(username='user2')]


@pytest.fixture
def create_user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user


@pytest.fixture
def categories():
    return [Category.objects.create(name='category1'), Category.objects.create(name='category2')]


@pytest.fixture
def client():
    return Client()