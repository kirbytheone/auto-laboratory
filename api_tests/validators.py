from jsonschema import validate

from api_tests.schemas.post_schema import POST_SCHEMA

def validate_status_code(response, expected_status_code: int):
    actual_status_code = response.status_code

    assert actual_status_code == expected_status_code, (
        f'Expected status code {expected_status_code}, '
        f'Actual status code {actual_status_code}. '
        f'Response body:{response.text}'
    )

def validate_response_field(response, field_name: str, expected_value):
    response_body = response.json()
    actual_value = response_body.get(field_name)

    assert actual_value == expected_value, (
        f'Expected value {field_name} should be {expected_value}, '
        f'Actual value {actual_value}. '
        f'Full response body: {response_body}'
    )

def validate_post_schema(response):
    response_body = response.json()

    validate(instance=response_body, schema=POST_SCHEMA)
