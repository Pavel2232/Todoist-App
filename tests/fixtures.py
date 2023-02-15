
import pytest


@pytest.fixture()
def client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
@pytest.mark.django_db
def test_user(django_user_model):
    user_data = {
        "username": 'ivan',
        "first_name": "test user first name",
        "last_name": "test user last name",
        "password": 'NormPassw0rd',
        "email": 'test@test.ru',
    }
    user = django_user_model.objects.create(**user_data)
    user.set_password(user.password)
    user.save()

    return user