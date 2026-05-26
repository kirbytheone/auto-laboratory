import pytest


@pytest.mark.django_db
def test_anonymous_user_redirect(client):
    response = client.get("/tasks/")

    assert response.status_code == 302