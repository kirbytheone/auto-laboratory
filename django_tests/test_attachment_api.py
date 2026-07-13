import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from tasks.models import Attachment


@pytest.mark.django_db
def test_auth_user_can_list_attachments_for_own_task(
        api_client,
        create_user,
        create_task,
        temporary_media_root,
):
    user = create_user(username='attachment_list_user')
    task = create_task(owner=user, title='Task with Attachment')

    uploaded_file = SimpleUploadedFile(
        name='existing_file.txt',
        content=b'Existing attachment',
        content_type='text/plain',
    )

    attachment = Attachment.objects.create(
        task=task,
        uploaded_by=user,
        file=uploaded_file,
    )

    api_client.force_authenticate(user=user)

    response = api_client.get(
        reverse(
            'api-task-attachment-list',
            kwargs={'task_pk': task.pk},
        )
    )

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == attachment.pk
    assert response.data[0]['filename'] == 'existing_file.txt'
    assert response.data[0]['uploaded_by'] == user.username

@pytest.mark.django_db
def test_auth_user_can_upload_attachment_to_own_task(
        api_client,
        create_user,
        create_task,
        temporary_media_root,
):
    user = create_user(username='attachment_upload_user')
    task = create_task(owner=user)

    api_client.force_authenticate(user=user)

    uploaded_file = SimpleUploadedFile(
        name='api_upload.txt',
        content=b"Uploaded attachment via API",
        content_type='text/plain',
    )

    response = api_client.post(
        reverse(
            'api-task-attachment-list',
            kwargs={'task_pk': task.pk},
        ),
        {
            'file': uploaded_file,
        },
        format='multipart',
    )

    assert response.status_code == 201

    attachment = Attachment.objects.get()

    assert attachment.task == task
    assert attachment.uploaded_by == user
    assert attachment.filename == 'api_upload.txt'

@pytest.mark.django_db
def test_auth_user_cannot_access_attachments_of_another_user_task(
        api_client,
        create_user,
        create_task,
):
    owner = create_user(username='attachment_owner')
    other_user = create_user(username='attachment_other_user')
    task = create_task(owner=owner)

    api_client.force_authenticate(user=other_user)

    response = api_client.get(
        reverse(
            'api-task-attachment-list',
            kwargs={'task_pk': task.pk},
        )
    )

    assert response.status_code == 404

@pytest.mark.django_db
def test_upload_attachment_requires_file(
        api_client,
        create_user,
        create_task,
        temporary_media_root,
):
    user = create_user(username='attachment_missing_file_user')
    task = create_task(owner=user)

    api_client.force_authenticate(user=user)

    response = api_client.post(
        reverse(
            'api-task-attachment-list',
            kwargs={'task_pk': task.pk},
        ),
        {},
        format='multipart',
    )

    assert response.status_code == 400
    assert 'file' in response.data
    assert Attachment.objects.count() == 0
