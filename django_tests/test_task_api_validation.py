import pytest

from django.urls import reverse

from tasks.models import Task


@pytest.mark.django_db
def test_create_task_requires_title(api_client, create_user):
    user = create_user(username='missing_task_title_user_api')
    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse('api-task-list'),
        {
            'description': 'Task without title',
            'status': Task.Status.TODO,
            'priority': Task.Priority.MEDIUM,
            'due_date': None,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'title' in response.data
    assert Task.objects.count() == 0

@pytest.mark.django_db
def test_create_task_rejects_invalid_status(api_client, create_user):
    user = create_user(username='invalid_status_user')
    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse('api-task-list'),
        {
            'title': 'Invalid Status Task',
            'description': '',
            'status': 'BLOCKED',
            'priority': Task.Priority.MEDIUM,
            'due_date': None,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'status' in response.data
    assert not Task.objects.filter(title='Invalid Status Task').exists()

@pytest.mark.django_db
def test_create_task_rejects_invalid_priority(api_client, create_user):
    user = create_user(username='invalid_priority_user')
    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse('api-task-list'),
        {
            'title': 'Invalid Priority Task',
            'description': '',
            'status': Task.Status.TODO,
            'priority': 'CRITICAL',
            'due_date': None,
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'priority' in response.data
    assert not Task.objects.filter(title='Invalid Priority Task').exists()

@pytest.mark.django_db
def test_create_task_rejects_invalid_due_date(api_client, create_user):
    user = create_user(username='invalid_due_date_user')
    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse('api-task-list'),
        {
            'title': 'Invalid Due Date Task',
            'description': '',
            'status': Task.Status.TODO,
            'priority': Task.Priority.MEDIUM,
            'due_date': 'not-a-date',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'due_date' in response.data
    assert not Task.objects.filter(title='Invalid Due Date Task').exists()
