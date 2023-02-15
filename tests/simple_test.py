import pytest
from django.urls import reverse
from rest_framework import status


def test_root_not_found(client):
    response = client.get("/")
    assert response.status_code == 404
