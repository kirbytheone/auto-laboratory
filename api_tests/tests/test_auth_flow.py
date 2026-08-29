def test_user_registration_returns_201(registered_user):
    response = registered_user['response']

    assert response.status_code == 201
