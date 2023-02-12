import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
def test_health_check(client):
    response = client.get(reverse('health-check'))
    assert response.status_code == status.HTTP_200_OK

