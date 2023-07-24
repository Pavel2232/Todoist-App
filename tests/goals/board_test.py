import pytest
from rest_framework.fields import DateTimeField

from goals.serializers import BoardSerializer
from tests.factories import BoardFactory
"""Тестирование Вью Досок"""



@pytest.mark.django_db
class TestBoard:
    def test_create_board(self, client, board, test_user):
        client.force_login(test_user)
        time = DateTimeField().to_representation
        expected_response = {
            "id": board.pk + 1,
            "created": time(board.created),
            "update": time(board.update),
            "title": "test_board",
            "is_deleted": False
        }
        data = {
            'title': 'test_board'
        }
        response = client.post("/goals/board/create", data=data)

        assert response.status_code == 201
        assert response.json() == expected_response
    # assert response.data["title"] == expected_response["title"]
    # assert response.data["is_deleted"] == False
    # assert response.data["id"] == expected_response["i


    @pytest.mark.django_db
    def test_detail_board(self, client, test_user):
        client.force_login(test_user)
        board = BoardFactory.create(with_owner=test_user)

        response = client.get(f"/goals/board/{board.id}")

        assert response.status_code == 200
        assert response.data == BoardSerializer(board).data


    @pytest.mark.django_db
    def test_deleted_board(self, client, test_user):
        client.force_login(test_user)
        board = BoardFactory.create(with_owner=test_user)

        response = client.delete(f"/goals/board/{board.id}")

        assert response.status_code == 204


    # @pytest.mark.django_db
    # def test_list_board(client,test_user):
    #     client.force_login(test_user)
    #     bords = BoardFactory.create_batch(10, with_owner=test_user)
    #
    #     response = client.get("/goals/board/list")
    #
    #     assert response.status_code == 200
    #     assert response.data == BoardListSerializer(bords, many=True).data




