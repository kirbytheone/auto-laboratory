import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

from tasks.models import Task, Comment, Attachment


@pytest.mark.django_db
def test_task_creation():
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Test TASK",
        description="Test description",
        status=Task.Status.TODO,
        priority=Task.Priority.MEDIUM,
        owner=user,
    )

    assert task.title == "Test TASK"
    assert task.description == "Test description"
    assert task.status == Task.Status.TODO
    assert task.priority == Task.Priority.MEDIUM
    assert task.owner == user

@pytest.mark.django_db
def test_comment_creation_for_task():
    user = User.objects.create_user(
        username="commentuser",
        password="testpassword123",
    )

    task = Task.objects.create(
        title="Test Task with comment",
        owner=user,
    )

    comment = Comment.objects.create(
        task=task,
        author=user,
        text="This is a test comment",
    )

    assert comment.task == task
    assert comment.author == user
    assert comment.text == "This is a test comment"
    assert task.comments.count() == 1
    assert task.comments.first() == comment

@pytest.mark.django_db
def test_deleting_task_related_comments():
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task with comments",
        owner=user,
    )

    Comment.objects.create(
        task=task,
        author=user,
        text="Comment 1",
    )

    Comment.objects.create(
        task=task,
        author=user,
        text="Comment 2",
    )

    assert Comment.objects.count() == 2

    task.delete()

    assert Comment.objects.count() == 0

@pytest.mark.django_db
def test_attachment_creation_for_task():
    user = User.objects.create_user(
        username="testuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task with attachment",
        owner=user,
    )

    uploaded_file = SimpleUploadedFile(
        name="test_file.txt",
        content=b"Test file content",
        content_type="text/plain",
    )

    attachment = Attachment.objects.create(
        task=task,
        uploaded_by=user,
        file=uploaded_file,
    )

    assert attachment.task == task
    assert attachment.uploaded_by == user
    assert attachment.filename.startswith("test_file")
    assert attachment.filename.endswith(".txt")
    assert task.attachments.count() == 1

@pytest.mark.django_db
def test_task_attachment_cascade_deletion():
    user = User.objects.create_user(
        username="attachmentcascadeuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task with attachment",
        owner=user,
    )

    uploaded_file = SimpleUploadedFile(
        name="delete_me.txt",
        content=b"Test file content",
        content_type="text/plain",
    )

    Attachment.objects.create(
        task=task,
        uploaded_by=user,
        file=uploaded_file,
    )

    assert Attachment.objects.count() == 1
    task.delete()
    assert Attachment.objects.count() == 0
























