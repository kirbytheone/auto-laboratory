import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from tasks.models import Task


@pytest.mark.django_db
def test_task_list_can_filter_by_status(client):
    user = User.objects.create_user(
        username="statusfilteruser",
        password="testpass123",
    )

    Task.objects.create(
        title="Todo Task",
        status=Task.Status.TODO,
        owner=user,
    )

    Task.objects.create(
        title="Done Task",
        status=Task.Status.DONE,
        owner=user,
    )

    client.login(
        username="statusfilteruser",
        password="testpass123",
    )

    response = client.get(
        reverse("task_list"),
        {"status": Task.Status.TODO},
    )

    assert response.status_code == 200
    assert b"Todo Task" in response.content
    assert b"Done Task" not in response.content

@pytest.mark.django_db
def test_task_list_can_filter_by_priority(client):
    user = User.objects.create_user(
        username="priorityfilteruser",
        password="testpass123",
    )

    Task.objects.create(
        title="Low Priority Task",
        priority=Task.Priority.LOW,
        owner=user,
    )

    Task.objects.create(
        title="High Priority Task",
        priority=Task.Priority.HIGH,
        owner=user,
    )

    client.login(
        username="priorityfilteruser",
        password="testpass123",
    )

    response = client.get(
        reverse("task_list"),
        {"priority": Task.Priority.HIGH},
    )

    assert response.status_code == 200
    assert b"High Priority Task" in response.content
    assert b"Low Priority Task" not in response.content

@pytest.mark.django_db
def test_task_list_can_filter_by_status_and_priority(client):
    user = User.objects.create_user(
        username="combinedfilteruser",
        password="testpass123",
    )

    Task.objects.create(
        title="Todo High Priority Task",
        status=Task.Status.TODO,
        priority=Task.Priority.HIGH,
        owner=user,
    )

    Task.objects.create(
        title="Todo Low Priority Task",
        status=Task.Status.TODO,
        priority=Task.Priority.LOW,
        owner=user,
    )

    Task.objects.create(
        title="Done High Priority Task",
        status=Task.Status.DONE,
        priority=Task.Priority.HIGH,
        owner=user,
    )

    client.login(
        username="combinedfilteruser",
        password="testpass123",
    )

    response = client.get(
        reverse("task_list"),
        {
            "status": Task.Status.TODO,
            "priority": Task.Priority.HIGH,
        },
    )

    assert response.status_code == 200
    assert b"Todo High Priority Task" in response.content
    assert b"Todo Low Priority Task" not in response.content
    assert b"Done High Priority Task" not in response.content
