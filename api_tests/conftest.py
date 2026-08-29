import pytest

from api_tests.clients.account_client import AccountClient
from api_tests.clients.tasks_client import TasksClient
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

    return {
        'payload': user_payload,
        'response': response,
    }

@pytest.fixture
def jwt_tokens(account_client, registered_user):
    payload = registered_user['payload']

    response = account_client.obtain_token_pair(
        username=payload['username'],
        password=payload['password'],
    )

    return response

@pytest.fixture
def authenticated_tasks_client(api_base_url, jwt_tokens):
    access_token = jwt_tokens.json()['access']

    client = TasksClient(api_base_url)
    client.session.headers.update(
        {
            'Authorization': f'Bearer {access_token}'
        }
    )

    return client

@pytest.fixture
def tasks_client(api_base_url):
    return TasksClient(api_base_url)
