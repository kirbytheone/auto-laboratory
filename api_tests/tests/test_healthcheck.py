import requests
from api_tests.clients.jsonplaceholder_client import JsonPlaceholderClient

## Health check
def test_healthcheck():
    response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

    assert response.status_code == 200
    assert response.json()["id"] == 1

## Using Class json client
def get_post_by_id():
    client = JsonPlaceholderClient()

    response_2 = client.get_post(1)
    assert response_2.status_code == 200
    assert response_2.json()["id"] == 1