import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
def test_logged_user_can_add_comment_to_task(client):
    user = User.objects.create_user(
        username="commentviewuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task For Comment",
        owner=user,
    )

    client.login(
        username="commentviewuser",
        password="testpass123",
    )

    response = client.post(
        reverse("add_comment", args=[task.pk]),
        {"text": "Comment from test"},
    )

    assert response.status_code == 302
    assert task.comments.count() == 1
    assert task.comments.first().text == "Comment from test"
