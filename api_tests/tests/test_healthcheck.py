import pytest

from api_tests.validators import *
from api_tests.data.post_payloads import get_create_post_payload

@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_id(json_placeholder_client, post_id):
    response = json_placeholder_client.get_post(post_id)

    validate_status_code(response, 200)
    validate_response_field(response, "id", post_id)
    validate_post_schema(response)

@pytest.mark.parametrize("post_id", [
    0, #boundary invalid value
    -1, # negative number
    9999, # non-existing request ID
])
def test_get_post_invalid_id(json_placeholder_client, post_id):
    response = json_placeholder_client.get_post(9999)

    validate_status_code(response, 404)

def test_create_post(json_placeholder_client):
    payload = get_create_post_payload(
        title='Test title',
        body='Test body',
        user_id=1,
    )
    response = json_placeholder_client.create_post(payload)

    validate_status_code(response, 201)
    validate_response_field(response, 'title', payload['title'])
    validate_response_field(response, 'body', payload['body'])
    validate_response_field(response, 'userId', payload['userId'])

@pytest.mark.parametrize("title, body, user_id", [
    ("Test_1 title", "Test_1 body", 1),
    ("Test_2 title", "Test_2 body", 2),
])
def test_create_post_multiple(json_placeholder_client, title, body, user_id):
    payload = get_create_post_payload(title, body, user_id)

    response = json_placeholder_client.create_post(payload)

    validate_status_code(response, 201)
    validate_response_field(response, 'title', title)
    validate_response_field(response, 'body', body)
    validate_response_field(response, 'userId', user_id)
