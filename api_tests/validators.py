def validate_status_code(response, expected_status_code: int):
    assert response.status_code == expected_status_code

def validate_response_field(response, field_name: str, expected_value):
    response_body = response.json()

    assert response_body[field_name] == expected_value
