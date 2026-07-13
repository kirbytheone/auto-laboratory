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

@pytest.mark.django_db
def test_auth_user_can_list_comments_for_task(api_client, create_user, create_task):
    user = create_user(username='comment_list_user')
    task = create_task(owner=user, title='Commented Task')

    Comment.objects.create(
        task=task,
        author=user,
        text='First API comment',
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse(
            'api-task-comment-list',
            kwargs={'task_pk': task.pk},
        )
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['text'] == 'First API comment'
    assert response.data[0]['author'] == user.username

@pytest.mark.django_db
def test_auth_user_can_create_comment_for_task(api_client, create_user, create_task):
    user = create_user(username='comment_api_create_user')
    task = create_task(owner=user)

    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse(
            'api-task-comment-list',
            kwargs={'task_pk': task.pk},
        ),
        {
            'text': 'Created API comment',
        },
        format='json',
    )

    assert response.status_code == 201

    comment = Comment.objects.get()

    assert comment.task == task
    assert comment.author == user
    assert comment.text == 'Created API comment'

@pytest.mark.django_db
def test_user_cannot_access_comments_for_another_user_task(api_client, create_user, create_task):
    owner = create_user(username='comment_owner_user')
    other_user = create_user(username='comment_other_user')
    task = create_task(owner=owner)

    api_client.force_authenticate(user=other_user)

    response = api_client.get(
        reverse(
            'api-task-comment-list',
            kwargs={'task_pk': task.pk},
        )
    )

    assert response.status_code == 404

@pytest.mark.django_db
def test_comment_rejects_empty_text(api_client, create_user, create_task):
    user = create_user(username='empty_comment_api_user')
    task = create_task(owner=user)

    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse(
            'api-task-comment-list',
            kwargs={'task_pk': task.pk},
        ),
        {
            'text': '',
        },
        format='json',
    )

    assert response.status_code == 400
    assert 'text' in response.data
    assert Comment.objects.count() == 0
