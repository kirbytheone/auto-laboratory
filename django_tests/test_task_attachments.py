import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from tasks.models import Task, Attachment


@pytest.mark.django_db
def test_logged_user_can_upload_attachment_to_task(client,
                                                   temporary_media_root):
    user = User.objects.create_user(
        username="attachmentviewuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task For Attachment",
        owner=user,
    )

    client.login(
        username="attachmentviewuser",
        password="testpass123",
    )

    uploaded_file = SimpleUploadedFile(
        name="view_upload.txt",
        content=b"Attachment from view test",
        content_type="text/plain",
    )

    response = client.post(
        reverse("upload_attachment", args=[task.pk]),
        {"file": uploaded_file},
    )

    assert response.status_code == 302
    assert Attachment.objects.count() == 1

    attachment = Attachment.objects.first()
    print(attachment.file.name)

    print(attachment.file.path)


    assert attachment.task == task
    assert attachment.uploaded_by == user
    assert attachment.filename.startswith("view_upload")
    assert attachment.filename.endswith(".txt")
