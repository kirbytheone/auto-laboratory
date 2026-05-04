import pytest

from api_tests.validators import *

@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_id(json_placeholder_client, post_id):
    response = json_placeholder_client.get_post(post_id)

    validate_status_code(response, 200)
    validate_response_field(response, "id", post_id)
