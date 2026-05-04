import pytest

from api_tests.validators import *

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
    payload = {
        'title': 'test POST title',
        'body': 'test POST body',
        'userId': 1,
    }

    response = json_placeholder_client.create_post(payload)

    validate_status_code(response, 201)
    validate_response_field(response, 'title', payload['title'])
    validate_response_field(response, 'body', payload['body'])
    validate_response_field(response, 'userId', payload['userId'])
