from api_tests.schemas.auth_schemas import (
    REGISTRATION_RESPONSE_SCHEMA,
    TOKEN_REFRESH_RESPONSE_SCHEMA,
    TOKEN_RESPONSE_SCHEMA,
)
from api_tests.validators import validate_schema


def test_user_registration_returns_201(registered_user):
    response = registered_user['response']

    assert response.status_code == 201

def test_registration_response_matches_contract(registered_user):
    response = registered_user['response']
    payload = registered_user['payload']

    validate_schema(
        response,
        REGISTRATION_RESPONSE_SCHEMA,
    )

    body = response.json()

    assert body['username'] == payload['username']
    assert body['email'] == payload['email']

def test_registered_user_can_obtain_jwt_tokens(jwt_tokens):
    assert jwt_tokens.status_code == 200

    validate_schema(
        jwt_tokens,
        TOKEN_RESPONSE_SCHEMA,
    )
    
def test_refresh_token_returns_new_access_token(account_client, jwt_tokens):
    refresh_token = jwt_tokens.json()['refresh']

    response = account_client.refresh_access_token(refresh_token)
    
    assert response.status_code == 200
    
    validate_schema(
        response,
        TOKEN_REFRESH_RESPONSE_SCHEMA,
    )

def test_access_token_allows_task_access(authenticated_tasks_client):
    response = authenticated_tasks_client.list_tasks()

    assert response.status_code == 200

def test_unauthenticated_task_access_returns_401(tasks_client):
    response = tasks_client.list_tasks()

    assert response.status_code == 401

def test_invalid_credentials_cannot_obtain_tokens(account_client, registered_user):
    payload = registered_user['payload']

    response = account_client.obtain_token_pair(
        username=payload['username'],
        password='WrongPassword123!',
    )

    assert response.status_code == 401

def test_duplicate_username_registration_returns_400(account_client, registered_user):
    payload = registered_user['payload']

    response = account_client.register(payload)

    assert response.status_code == 400
    assert 'username' in response.json()

def test_invalid_access_token_is_rejected(tasks_client):
    tasks_client.session.headers.update(
        {
            'Authorization': 'Bearer definitely-invalid-token'
        }
    )

    response = tasks_client.list_tasks()
    assert response.status_code == 401
