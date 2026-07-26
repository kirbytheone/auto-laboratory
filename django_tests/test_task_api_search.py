import pytest

from django.urls import reverse


@pytest.mark.django_db
def test_task_api_search_by_title(api_client, create_user, create_task):
    user = create_user(username='title_search_user')

    create_task(
        owner=user,
        title='Prepare Interview',
        description='Review Python'
    )
    create_task(
        owner=user,
        title='Buy Groceries',
        description='Milk and bread',
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'search': 'Interview'},
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Prepare Interview'

@pytest.mark.django_db
def test_task_api_search_by_description(api_client, create_user, create_task):
    user = create_user(username='description_search_user')

    create_task(
        owner=user,
        title='Study',
        description='Practice Playwright automation',
    )
    create_task(
        owner=user,
        title='Training',
        description='Mobility and Recovery',
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'search': 'Playwright automation'},
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Study'

@pytest.mark.django_db
def test_task_api_search_is_case_insensitive(api_client, create_user, create_task):
    user = create_user(username='insensitive_case_search_user')

    create_task(
        owner=user,
        title='Python Practice',
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'search': 'python'},
    )

    assert response.status_code == 200
    assert response.data['count'] == 1

@pytest.mark.django_db
def test_task_api_search_only_auth_users_tasks(api_client, create_user, create_task):
    user = create_user(username='search_owner')
    other_user = create_user(username='other_user_search')

    create_task(
        owner=user,
        title='Private Automation Task',
    )
    create_task(
        owner=other_user,
        title='Other Automation Task',
    )

    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse('api-task-list'),
        {'search': 'Automation'},
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Private Automation Task'
