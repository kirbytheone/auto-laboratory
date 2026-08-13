import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_valid_refresh_token_returns_new_access_token(api_client, create_user):
    create_user(
        username='refresh_user_access_token',
        password='securepass123',
    )

    token_response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'refresh_user_access_token',
            'password': 'securepass123',
        },
        format='json',
    )
    assert token_response.status_code == 200
    refresh_token = token_response.json()['refresh']

    refresh_response = api_client.post(
        reverse('token_refresh'),
        {'refresh': refresh_token,
         },
        format='json',
    )

    assert refresh_response.status_code == 200
    assert 'access' in refresh_response.data
    assert refresh_response.data['access']

@pytest.mark.django_db
def test_refresh_token_cannot_authenticate_task_api(api_client, create_user, create_task):
    user = create_user(
        username='refresh_auth_user',
        password='securepass123',
    )
    create_task(
        owner=user,
        title='Protected Task',
    )

    token_response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'refresh_auth_user',
            'password': 'securepass123',
        },
        format='json',
    )
    assert token_response.status_code == 200
    refresh_token = token_response.json()['refresh']

    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {refresh_token}'
    )

    response = api_client.get(reverse('api-task-list'))

    assert response.status_code == 401

@pytest.mark.django_db
def test_session_authentication_does_not_allow_api_access(api_client, create_user):
    create_user(
        username='session_user',
        password='securepass123',
    )

    logged_in = api_client.login(
        username='session_user',
        password='securepass123',
    )

    assert logged_in is True

    response = api_client.get(reverse('api-task-list'))

    assert response.status_code == 401

@pytest.mark.django_db
def test_user_can_obtain_jwt_token(api_client, create_user):
    create_user(
        username='token_user',
        password='securepass123',
    )

    response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'token_user',
            'password': 'securepass123',
        },
        format='json',
    )

    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['access']
    assert response.data['refresh']

@pytest.mark.django_db
def test_jwt_tokens_cannot_be_obtained_with_invalid_auth(api_client, create_user):
    create_user(
        username='invalid_token_user',
        password='correctpass123',
    )

    response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'invalid_token_user',
            'password': 'wrongpass123',
        },
        format='json',
    )

    assert response.status_code == 401
    assert 'access' not in response.data
    assert 'refresh' not in response.data
    assert 'detail' in response.data

@pytest.mark.django_db
def test_inactive_user_cannot_obtain_jwt_tokens(
        api_client,
        create_user,
):
    user = create_user(
        username='inactive_user',
        password='securepass123',
    )

    user.is_active = False
    user.save()

    response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'inactive_user',
            'password': 'securepass123',
        },
        format='json',
    )

    assert response.status_code == 401
    assert 'access' not in response.data
    assert 'refresh' not in response.data

@pytest.mark.django_db
def test_access_token_allows_access_to_task_api(api_client, create_user, create_task):
    user = create_user(
        username='token_access_user',
        password='securepass123',
    )
    create_task(
        owner=user,
        title='Token Protected Task',
    )

    token_response = api_client.post(
        reverse('token_obtain_pair'),
        {
            'username': 'token_access_user',
            'password': 'securepass123',
        },
        format='json',
    )
    assert token_response.status_code == 200
    access_token = token_response.json()['access']

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Token Protected Task'

@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_task_api(api_client):
    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 401
    assert response.data['detail'] == 'Authentication credentials were not provided.'

@pytest.mark.django_db
def test_invalid_jwt_token_is_rejected(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid-value')

    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 401

@pytest.mark.django_db
def test_legacy_token_auth_is_rejected(api_client):
    api_client.credentials(HTTP_AUTHORIZATION='Token invalid-value')

    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 401
    assert 'detail' in response.data
