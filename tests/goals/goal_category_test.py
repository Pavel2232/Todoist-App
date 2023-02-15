import pytest

from goals.serializers import GoalCategorySerializer
from tests.factories import BoardFactory, GoalCategoryFactory

"""Тестирование Вью Категорий"""
@pytest.mark.django_db
def test_create_category(client, goal_category, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    expected_response = {
        "id": goal_category.id + 1,
        "board": board.id,
        "title": "test_category",
    }
    data = {
        'title': "test_category",
        'board': board.id
    }
    response = client.post("/goals/goal_category/create", data=data)

    assert response.status_code == 201
    assert response.data["title"] == expected_response["title"]
    assert response.data["is_deleted"] == False
    assert response.data["id"] == expected_response["id"]


@pytest.mark.django_db
def test_detail_category(client, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)

    response = client.get(f"/goals/goal_category/{category.id}")

    assert response.status_code == 200
    assert response.data == GoalCategorySerializer(category).data


@pytest.mark.django_db
def test_deleted_category(client, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)

    response = client.delete(f"/goals/goal_category/{category.id}")

    assert response.status_code == 204


@pytest.mark.django_db
def test_patch_category(client, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    expected_response = {
        "id": category.id,
        "board": board.id,
        "title": "NewTitle",
    }
    data = {
        'title': "NewTitle",
        'board': board.id
    }
    response= client.patch(f"/goals/goal_category/{category.id}", data=data)

    assert response.status_code == 200
    assert response.data["title"] == expected_response["title"]
    assert response.data["is_deleted"] == False
    assert response.data["id"] == expected_response["id"]
