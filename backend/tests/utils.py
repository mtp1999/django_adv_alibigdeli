import pytest
from rest_framework.test import APIClient
from app_account.models import User


@pytest.fixture
def test_user1(db):
    user1 = User.objects.create_user(email='user1@gmail.com', password='a123456d')
    return user1


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def api_client_authenticated(test_user1):
    client = APIClient()
    client.force_authenticate(user=test_user1)
    return client


def validate_keys(expected_keys: list, dict_keys: list):
    assert list(expected_keys).sort() == list(dict_keys).sort()

