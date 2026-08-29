import pytest

from api_tests.clients.account_client import AccountClient
from api_tests.config import API_TEST_BASE_URL
from api_tests.data.user_factory import build_user_payload


@pytest.fixture
def api_base_url():
    return API_TEST_BASE_URL

@pytest.fixture
def account_client(api_base_url):
    return AccountClient(api_base_url)

@pytest.fixture
def user_payload():
    return build_user_payload()

@pytest.fixture
def registered_user(account_client, user_payload):
    response = account_client.register(user_payload)

    assert response.status_code == 201

    return {
        'payload': user_payload,
        'response': response,
    }