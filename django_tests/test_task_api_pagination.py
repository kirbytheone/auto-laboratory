import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_task_api_uses_default_page_size(api_client, create_user, create_task):
    user = create_user(username="pagination_user")

    for index in range(5):
        create_task(
            owner=user,
            title=f'Task {index + 1}',
        )

    api_client.force_authenticate(user=user)

    response = api_client.get(reverse('api-task-list'))

    assert response.status_code == 200
    assert response.data['count'] == 5
    assert len(response.data['results']) == 3
    assert response.data['next'] is not None
    assert response.data['previous'] is None

@pytest.mark.django_db
def test_task_api_returns_second_page(api_client, create_user, create_task):
    user = create_user(username="second_page_user")

    for index in range(5):
        create_task(
            owner=user,
            title=f'Task {index + 1}'
        )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'page': 2},
    )

    assert response.status_code == 200
    assert response.data['count'] == 5
    assert len(response.data['results']) == 2
    assert response.data['next'] is None
    assert response.data['previous'] is not None

@pytest.mark.django_db
def test_task_api_rejects_page_out_of_range(api_client, create_user, create_task):
    user = create_user(username="invalid_page_user")
    create_task(owner=user)

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'page': 999},
    )

    assert response.status_code == 404
    assert 'detail' in response.data

@pytest.mark.django_db
def test_pagination_counts_only_authenticated_users_tasks(api_client, create_user, create_task):
    user = create_user(username="pagination_owner_user")
    other_user = create_user(username="pagination_other_user")

    for index in range(4):
        create_task(
            owner=user,
            title=f'Owner Task {index + 1}',
        )

    for index in range(3):
        create_task(
            owner=other_user,
            title=f'Other Task {index + 1}',
        )

    api_client.force_authenticate(user=user)
    response = api_client.get(reverse('api-task-list'))

    assert response.status_code == 200
    assert response.data['count'] == 4
    assert len(response.data['results']) == 3

    returned_titles = {
        task['title'] for task in response.data['results']
    }

    assert all(
        title.startswith('Owner Task') for title in returned_titles
    )
