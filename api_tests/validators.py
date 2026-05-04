from jsonschema import validate

from api_tests.schemas.post_schema import POST_SCHEMA

def validate_status_code(response, expected_status_code: int):
    assert response.status_code == expected_status_code

def validate_response_field(response, field_name: str, expected_value):
    response_body = response.json()

    assert response_body[field_name] == expected_value

def validate_post_schema(response):
    validate(instance=response.json(), schema=POST_SCHEMA)

# def validate_post_schema(response):
#     response_body = response.json()
#
#     assert "userId" in response_body
#     assert "id" in response_body
#     assert "title" in response_body
#     assert "body" in response_body
#
#     assert isinstance(response_body["userId"], int)
#     assert isinstance(response_body["id"], int)
#     assert isinstance(response_body["title"], str)
#     assert isinstance(response_body["body"], str)
