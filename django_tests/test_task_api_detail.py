import pytest

from django.urls import reverse

from tasks.models import Task


@pytest.mark.django_db
def test_auth_user_can_retrieve_own_tasks(api_client, create_user, create_task):
    user = create_user(username="test_api_user")
    task = create_task(owner=user, title='Task created via API')
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse("api-task-detail", kwargs={'pk': task.pk}))

    assert response.status_code == 200
    assert response.data['id'] == task.pk
    assert response.data['title'] == 'Task created via API'

@pytest.mark.django_db
def test_user_cannot_access_another_user_tasks(api_client, create_user, create_task):
    task_owner = create_user(username='api_task_owner')
    other_user = create_user(username='task_api_other_user')
    task = create_task(owner=task_owner, title='User API task')

    api_client.force_authenticate(user=other_user)

    response = api_client.get(
        reverse('api-task-detail', kwargs={'pk': task.id})
    )

    assert response.status_code == 404

@pytest.mark.django_db
def test_auth_user_can_patch_own_task(api_client, create_user, create_task):
    user = create_user(username="patch_api_user")
    task = create_task(
        owner=user,
        title='API Title',
        priority=Task.Priority.LOW)

    api_client.force_authenticate(user=user)

    response = api_client.patch(
        reverse('api-task-detail', kwargs={'pk': task.id}),
        {
            'title': 'Updated API title',
            'priority': Task.Priority.HIGH,
        },
        format='json',
    )

    assert response.status_code == 200

    task.refresh_from_db()

    assert task.title == 'Updated API title'
    assert task.priority == Task.Priority.HIGH

@pytest.mark.django_db
def test_auth_user_can_delete_own_task(api_client, create_user, create_task):
    user = create_user(username="delete_api_user")
    task = create_task(owner=user, title='Delete Through API')

    api_client.force_authenticate(user=user)

    response = api_client.delete(
        reverse('api-task-detail', kwargs={'pk': task.id})
    )

    assert response.status_code == 204
    assert not Task.objects.filter(pk=task.pk).exists()

@pytest.mark.django_db
def test_user_cannot_update_another_users_task(api_client, create_user, create_task):
    owner = create_user(username="update_api_owner")
    other_user = create_user(username="update_api_other_user")
    task = create_task(
        owner=owner,
        title='Task Title',
        priority=Task.Priority.LOW,
    )

    api_client.force_authenticate(user=other_user)

    response = api_client.patch(
        reverse('api-task-detail', kwargs={'pk': task.id}),
        {
            'title': 'Unauthorized Change',
            'priority': Task.Priority.HIGH,
        },
        format='json',
    )

    assert response.status_code == 404

    task.refresh_from_db()

    assert task.title == 'Task Title'
    assert task.priority == Task.Priority.LOW

@pytest.mark.django_db
def test_user_cannot_delete_another_users_task(api_client, create_user, create_task):
    owner = create_user(username="delete_api_owner")
    other_user = create_user(username="delete_api_other_user")
    task = create_task(
        owner=owner,
        title='Protected Delete API Task'
    )

    api_client.force_authenticate(user=other_user)

    response = api_client.delete(
        reverse('api-task-detail', kwargs={'pk': task.id})
    )

    assert response.status_code == 404
    assert Task.objects.filter(pk=task.pk).exists()
