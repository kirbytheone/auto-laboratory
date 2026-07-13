import pytest

from django.urls import reverse

from tasks.models import Comment, Task


@pytest.mark.django_db
def test_anonymous_user_cannot_access_task_api(api_client):
    response = api_client.get(reverse("api-task-list"))

    assert response.status_code == 403

@pytest.mark.django_db
def test_auth_user_can_list_own_tasks_api(api_client, create_user, create_task):
    user = create_user(username="test_api_user")
    other_user = create_user(username="other_api_user")

    user_task = create_task(owner=user, title='User API task')
    create_task(owner=other_user, title='Other user API task')

    api_client.force_authenticate(user=user)

    response = api_client.get(reverse("api-task-list"))

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == user_task.id
    assert response.data[0]['title'] == 'User API task'

@pytest.mark.django_db
def test_auth_user_can_create_task(api_client, create_user):
    user = create_user(username="test_api_user")

    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse('api-task-list'),
        {
            'title': 'Task created via API',
            'description': 'Django REST test',
            'status': Task.Status.TODO,
            'priority': Task.Priority.HIGH,
            'due_date': None,
        },
        format='json',
    )

    assert response.status_code == 201

    task = Task.objects.get(title='Task created via API')

    assert task.owner == user
    assert task.priority == Task.Priority.HIGH

@pytest.mark.django_db
def test_user_client_cannot_override_task_owner(api_client, create_user):
    user = create_user(username='real_owner')
    other_user = create_user(username='other_user')

    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse('api-task-list'),
        {
            'title': 'Ownership Test Task',
            'description': '',
            'status': Task.Status.TODO,
            'priority': Task.Priority.MEDIUM,
            'due_date': None,
            'owner': other_user.id,
        },
        format='json',
    )

    assert response.status_code == 201

    task = Task.objects.get(title='Ownership Test Task')

    assert task.owner == user
    assert task.owner != other_user
