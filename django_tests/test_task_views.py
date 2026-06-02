import pytest
from django.contrib.auth.models import User
from tasks.models import Task


@pytest.mark.django_db
def test_anonymous_user_redirect(client):
    response = client.get("/tasks/")

    assert response.status_code == 302

@pytest.mark.django_db
def test_logged_user_able_view_task_list(client):
    user = User.objects.create_user(
        username="viewuser",
        password="testpass123",
    )

    Task.objects.create(
        title="Visible Task",
        owner=user,
    )

    login_successful = client.login(
        username="viewuser",
        password="testpass123",
    )

    assert login_successful is True
    response = client.get("/tasks/")

    assert response.status_code == 200
    assert b"Visible Task" in response.content

@pytest.mark.django_db
def test_task_list_shows_only_logged_users_tasks(client):
    user = User.objects.create_user(
        username="owneruser",
        password="testpass123",
    )

    other_user = User.objects.create_user(
        username="otheruser",
        password="testpass123",
    )

    Task.objects.create(
        title="My Task",
        owner=user,
    )

    Task.objects.create(
        title="Other User Task",
        owner=other_user,
    )

    client.login(
        username="owneruser",
        password="testpass123",
    )

    response = client.get("/tasks/")

    assert response.status_code == 200
    assert b"My Task" in response.content
    assert b"Other User Task" not in response.content

@pytest.mark.django_db
def test_logged_in_user_can_create_task(client):
    user = User.objects.create_user(
        username="createuser",
        password="testpass123",
    )

    client.login(
        username="createuser",
        password="testpass123",
    )

    response = client.post(
        "/tasks/create/",
        {
            "title": "Created From Test",
            "description": "Created using Django test client",
            "priority": Task.Priority.HIGH,
            "due_date": "2026-05-20",
        },
    )

    assert response.status_code == 302
    assert Task.objects.count() == 1

    task = Task.objects.first()

    assert task.title == "Created From Test"
    assert task.description == "Created using Django test client"
    assert task.priority == Task.Priority.HIGH
    assert task.due_date.isoformat() == "2026-05-20"
    assert task.owner == user

@pytest.mark.django_db
def test_user_can_create_task_with_no_due_date(client):
    user = User.objects.create_user(
        username="createdatenoneuser",
        password="testpass123",
    )

    client.login(
        username="createdatenoneuser",
        password="testpass123",
    )

    response = client.post(
        "/tasks/create/",
        {
            "title": "Task Without Due Date",
            "description": "No deadline",
            "priority": Task.Priority.MEDIUM,
            "due_date": "",
        },
    )

    assert response.status_code == 302

    task = Task.objects.first()

    assert task.title == "Task Without Due Date"
    assert task.due_date is None

@pytest.mark.django_db
def test_logged_user_can_view_task_details(client):
    user = User.objects.create_user(
        username="detailuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Detailed Task",
        description="Task detail description",
        status=Task.Status.IN_PROGRESS,
        priority=Task.Priority.HIGH,
        owner=user,
    )

    login_successful = client.login(
        username="detailuser",
        password="testpass123",
    )

    assert login_successful is True

    response = client.get(f"/tasks/{task.id}/")

    assert response.status_code == 200
    assert b"Detailed Task" in response.content
    assert b"Task detail description" in response.content
    assert b"IN_PROGRESS" in response.content
    assert b"HIGH" in response.content

@pytest.mark.django_db
def test_logged_user_can_open_edit_task_page(client):
    user = User.objects.create_user(
        username="editpageuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task To Edit",
        description="Old description",
        status=Task.Status.TODO,
        priority=Task.Priority.LOW,
        owner=user,
    )

    login_successful = client.login(
        username="editpageuser",
        password="testpass123",
    )

    assert login_successful is True

    response = client.get(f"/tasks/{task.id}/edit/")

    assert response.status_code == 200
    assert b"Edit Task" in response.content
    assert b"Task To Edit" in response.content
    assert b"Old description" in response.content

@pytest.mark.django_db
def test_logged_user_can_update_task(client):
    user = User.objects.create_user(
        username="updatetaskuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Old Task Title",
        description="Old Description",
        status=Task.Status.TODO,
        priority=Task.Priority.LOW,
        owner=user,
    )

    login_successful = client.login(
        username="updatetaskuser",
        password="testpass123",
    )

    assert login_successful is True

    response = client.post(
        f"/tasks/{task.id}/edit/",
        {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": Task.Status.DONE,
            "priority": Task.Priority.HIGH,
            "due_date": "2026-06-01",
        },
    )

    assert response.status_code == 302

    task.refresh_from_db()

    assert task.title == "Updated Task Title"
    assert task.description == "Updated description"
    assert task.status == Task.Status.DONE
    assert task.priority == Task.Priority.HIGH
    assert task.due_date.isoformat() == "2026-06-01"

@pytest.mark.django_db
def test_logged_user_can_delete_task(client):
    user = User.objects.create_user(
        username="deletetaskuser",
        password="testpass123",
    )

    task = Task.objects.create(
        title="Task To Delete",
        owner=user,
    )

    login_successful = client.login(
        username="deletetaskuser",
        password="testpass123",
    )

    assert login_successful is True
    assert Task.objects.count() == 1

    response = client.post(
        f"/tasks/{task.id}/delete/"
    )

    assert response.status_code == 302
    assert Task.objects.count() == 0
