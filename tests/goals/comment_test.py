import pytest

from goals.serializers import CommentSerializer
from tests.factories import BoardFactory, GoalCategoryFactory, GoalFactory, CommentFactory
"""Тесты Вью Комментариев"""

@pytest.mark.django_db
def test_create_comment(client, goal_comment, test_user):
    client.force_login(test_user)
    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    goal = GoalFactory.create(user=test_user, category=category)
    expected_response = {
        "id": goal_comment.id + 1,
        "goal": goal.id,
        "text": goal_comment.text,
    }
    data = {
        'goal': goal.id,
        'text': goal_comment.text
    }
    response = client.post("/goals/goal_comment/create", data=data)

    assert response.status_code == 201
    assert response.data["text"] == expected_response["text"]
    assert response.data["id"] == expected_response["id"]


@pytest.mark.django_db
def test_detail_comment(client, test_user):
    client.force_login(test_user)

    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    goal = GoalFactory.create(user=test_user, category=category)
    comment = CommentFactory.create(goal=goal, user=test_user)

    response = client.get(f"/goals/goal_comment/{comment.id}")

    assert response.status_code == 200
    assert response.data == CommentSerializer(comment).data


@pytest.mark.django_db
def test_deleted_comment(client, test_user):
    client.force_login(test_user)

    board = BoardFactory.create(with_owner=test_user)
    category = GoalCategoryFactory.create(user=test_user, board=board)
    goal = GoalFactory.create(user=test_user, category=category)
    comment = CommentFactory.create(goal=goal, user=test_user)

    response = client.delete(f"/goals/goal_comment/{comment.id}")

    assert response.status_code == 204
