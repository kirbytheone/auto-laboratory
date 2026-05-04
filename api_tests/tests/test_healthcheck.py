import pytest


@pytest.mark.parametrize("post_id", [1, 2, 3])
def test_get_post_by_id(json_placeholder_client, post_id):
    response = json_placeholder_client.get_post(post_id)

    assert response.status_code == 200
    assert response.json()["id"] == post_id
