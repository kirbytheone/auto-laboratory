import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_user_can_obtain_api_token(api_client, create_user):
    create_user(
        username='token_user',
        password='securepass123',
    )

    response = api_client.post(
        reverse('api-token'),
        {
            'username': 'token_user',
            'password': 'securepass123',
        },
        format='json',
    )

    assert response.status_code == 200
    assert 'token' in response.data
    assert response.data['token']

@pytest.mark.django_db
def test_token_cannot_be_obtained_with_invalid_auth(api_client, create_user):
    create_user(
        username='invalid_token_user',
        password='correctpass123',
    )

    response = api_client.post(
        reverse('api-token'),
        {
            'username': 'invalid_token_user',
            'password': 'wrongpass123',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'token' not in response.data

@pytest.mark.django_db
def test_token_allows_access_to_task_api(api_client, create_user, create_task):
    user = create_user(
        username='token_access_user',
        password='securepass123',
    )
    create_task(
        owner=user,
        title='Token Protected Task',
    )

    token_response = api_client.post(
        reverse('api-token'),
        {
            'username': 'token_access_user',
            'password': 'securepass123',
        },
        format='json',
    )

    token = token_response.json()['token']

    api_client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Token Protected Task'

@pytest.mark.django_db
def test_invalid_token_rejected(api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f'Token invalid-value')

    response = api_client.get(
        reverse('api-task-list')
    )

    assert response.status_code == 401
    assert 'detail' in response.data
