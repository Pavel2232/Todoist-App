import pytest


@pytest.mark.django_db
def test_create_goal_category(client, test_user):#, user_token):
    x=1
    client.force_login(test_user)

    expected_respone = {


    }