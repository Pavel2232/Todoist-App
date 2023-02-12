
import pytest


@pytest.fixture()
def client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture()
@pytest.mark.django_db
def user_token(client, django_user_model):
    username = "test1"
    email = "test@test.ru"
    password = "10203040x"

    django_user_model.objects.create_user(
        username=username, password=password, email=email)

    response = client.post(
        "/core/login",
        {"username": username, "password": password},
        format='json'
    )

    return response.data["sessionid"]

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