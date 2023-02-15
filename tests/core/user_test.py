import pytest
from rest_framework import status

from tests.factories import UserFactory

"""Тесты Вью Пользователя"""


@pytest.mark.django_db
def test_signup_user(client, test_user):
    expected_response = {
        "id": test_user.id + 1,
        "email": "Test@example.com",
        "first_name": "Test_first",
        "last_name": "Test_last",
        "username": "Test_username"
    }

    data = {
        "email": "Test@example.com",
        "password": "NormalPass2",
        "password_repeat": "NormalPass2",
        "first_name": "Test_first",
        "last_name": "Test_last",
        "username": "Test_username"
    }
    response = client.post("/core/signup", data=data)

    assert response.status_code == 201
    assert response.json() == expected_response


@pytest.mark.django_db
def test_login_user(client):
    UserFactory.create(username='Victor', password='10203040x')
    response = client.post('/core/login', data={
        'username': 'Victor',
        'password': '10203040x',
    })
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_not_login(client):
    UserFactory.create(username='Victor', password='10203040x')
    response = client.post('/core/login', data={
        'username': 'UserNotCorrectLogin',
        'password': '10203040x',
    })
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_patch_user(client, test_user):
    client.force_login(test_user)
    extend_response = {
        "id": test_user.id,
        "email": 'luboy@mail.ru',
        "username": test_user.username,
        "first_name": test_user.first_name,
        "last_name": test_user.last_name
    }
    response = client.patch('/core/profile', data={
        'email': 'luboy@mail.ru'
    })
    assert response.status_code == status.HTTP_200_OK
    assert extend_response == response.json()


@pytest.mark.django_db
def test_changes_password(client, test_user):
    client.force_login(test_user)
    new_password = '10203040x'

    response = client.put('/core/update_password', data={
        "new_password": new_password,
        "old_password": 'NormPassw0rd'
    })

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_signup_not_valid_password_user(client, test_user):
    data = {
        "email": "Test@example.com",
        "password": "qwerty123",
        "password_repeat": "qwerty123",
        "first_name": "Test_first",
        "last_name": "Test_last",
        "username": "Test_username"
    }
    response = client.post("/core/signup", data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
