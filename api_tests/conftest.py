import pytest

from api_tests.clients.jsonplaceholder_client import JsonPlaceholderClient

@pytest.fixture
def json_placeholder_client():
    return JsonPlaceholderClient()