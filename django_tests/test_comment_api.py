import pytest

from django.urls import reverse

from tasks.models import Comment, Task


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
