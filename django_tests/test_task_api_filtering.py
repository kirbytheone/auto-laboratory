import pytest
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
def test_task_api_filters_by_status(api_client, create_user, create_task):
    user = create_user(username='status_filter_user')

    create_task(
        owner=user,
        title='Todo Task',
        status=Task.Status.TODO,
    )
    create_task(
        owner=user,
        title='Done Task',
        status=Task.Status.DONE,
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'status': Task.Status.TODO},
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Todo Task'

@pytest.mark.django_db
def test_task_api_filters_by_priority(api_client, create_user, create_task):
    user = create_user(username='priority_filter_user')

    create_task(
        owner=user,
        title='Low Priority Task',
        priority=Task.Priority.LOW,
    )
    create_task(
        owner=user,
        title='High Priority Task',
        priority=Task.Priority.HIGH,
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse('api-task-list'),
        {'priority': Task.Priority.HIGH},
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'High Priority Task'

@pytest.mark.django_db
def test_task_api_filters_by_status_and_priority(api_client, create_user, create_task):
    user = create_user(username='combined_filter_user')

    create_task(
        owner=user,
        title='Todo High Priority Task',
        status=Task.Status.TODO,
        priority=Task.Priority.HIGH,
    )
    create_task(
        owner=user,
        title='Todo Low Priority Task',
        status=Task.Status.TODO,
        priority=Task.Priority.LOW,
    )
    create_task(
        owner=user,
        title='Done High Priority Task',
        status=Task.Status.DONE,
        priority=Task.Priority.HIGH,
    )

    api_client.force_authenticate(user=user)
    response = api_client.get(
        reverse('api-task-list'),
        {
            'status': Task.Status.TODO,
            'priority': Task.Priority.HIGH,
        },
    )

    assert response.status_code == 200
    assert response.data['count'] == 1
    assert response.data['results'][0]['title'] == 'Todo High Priority Task'
