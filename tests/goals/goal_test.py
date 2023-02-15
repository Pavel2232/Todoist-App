import pytest

from goals.serializers import GoalSerializer
from tests.factories import BoardFactory, GoalCategoryFactory, GoalFactory

"""Тесты Вью Целей"""
@pytest.mark.django_db
def test_create_goal(client, goal, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    expected_response = {
        "id": goal.id + 1,
        "category": category.id,
        "title": "test_goal",
    }
    data = {
        'title': 'test_goal',
        'category': category.id,
    }
    response = client.post("/goals/goal/create", data=data)

    assert response.status_code == 201
    assert response.data["title"] == expected_response["title"]
    assert response.data["id"] == expected_response["id"]
    assert response.data["category"] == expected_response["category"]


@pytest.mark.django_db
def test_detail_goal(client, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    goal = GoalFactory.create(user=test_user, category=category)

    response = client.get(f"/goals/goal/{goal.id}")

    assert response.status_code == 200
    assert response.data == GoalSerializer(goal).data


@pytest.mark.django_db
def test_deleted_goal(client, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    goal = GoalFactory.create(user=test_user, category=category)

    response = client.delete(f"/goals/goal/{goal.id}")

    assert response.status_code == 204


@pytest.mark.django_db
def test_patch_goal(client, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    goal = GoalFactory.create(user=test_user, category=category)

    expected_response = {
        "id": goal.id,
        "category": category.id,
        "title": "NewTitle",
    }

    data = {
        'title': 'NewTitle'
    }
    response = client.patch(f"/goals/goal/{goal.id}", data=data)

    assert response.status_code == 200
    assert response.data["title"] == expected_response["title"]
    assert response.data["id"] == expected_response["id"]
