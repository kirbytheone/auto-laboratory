import pytest

from tasks.models import Task


@pytest.mark.django_db
def test_user_cannot_view_other_user_task_details(client, create_user, create_task):
    owner = create_user(username='owner')
    other_user = create_user(username='other_user')
    task = create_task(owner=owner, title="private Task")

    client.force_login(other_user)

    response = client.get(f"/tasks/{task.id}/")

    assert response.status_code == 404

@pytest.mark.django_db
def test_user_cannot_edit_other_users_task_details(client, create_user, create_task):
    owner = create_user(username="owner")
    other_user = create_user(username="other_user")
    task = create_task(owner=owner, title="Private Task")

    client.force_login(other_user)

    response = client.post(
        f"/tasks/{task.id}/edit/",
        {
            "title": "Hacked Task",
            "description": "Unauthorized edit",
            "ststus": "done",
            "priority": "high",
            "due_date": "",
        },
    )
    assert response.status_code == 404
    task.refresh_from_db()
    assert task.title == "Private Task"

@pytest.mark.django_db
def test_user_cannot_delete_others_users_task(client, create_user, create_task):
    owner = create_user(username="owner")
    other_user = create_user(username="other_user")
    task = create_task(owner=owner, title="Private Task")

    client.force_login(other_user)

    response = client.post(f"/tasks/{task.id}/delete/")

    assert response.status_code == 404
    assert Task.objects.filter(id=task.id).exists()
