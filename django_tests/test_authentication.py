import pytest

from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_user_can_register(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()

    user = User.objects.get(username="newuser")

    assert user.email == "newuser@example.com"
    assert user.is_authenticated

    response = client.get(reverse("task_list"))

    assert response.context["user"].is_authenticated

@pytest.mark.django_db
def test_registered_password_is_hashed(client):
    raw_password = "StrongPass123!"

    client.post(
        reverse("register"),
        {
            "username": "secureuser",
            "email": "secureuser@example.com",
            "password1": raw_password,
            "password2": raw_password,
        },
    )

    user = User.objects.get(username="secureuser")

    assert user.password != raw_password
    assert user.check_password(raw_password) is True

@pytest.mark.django_db
def test_user_can_login(client):
    User.objects.create_user(
        username="loginuser",
        password="StrongPass123!",
    )

    response = client.post(
        reverse("login"),
        {
            "username": "loginuser",
            "password": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert "_auth_user_id" in client.session

@pytest.mark.django_db
def test_user_can_logout(client):
    user = User.objects.create_user(
        username="logoutuser",
        password="StrongPass123!",
    )
    client.force_login(user)
    response = client.post(
        reverse("logout"),
    )

    assert response.status_code == 302
    assert "_auth_user_id" not in client.session

@pytest.mark.django_db
def test_registration_rejects_duplicate_email_case_sense(client):
    User.objects.create_user(
        username="existing_user",
        email="existing@example.com",
        password="StrongPass123!",
    )

    response = client.post(
        reverse("register"),
        {
            "username": "new_user",
            "email": "EXISTING@EXAMPLE.COM",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 200
    assert not User.objects.filter(username="new_user").exists()
    assert (
            'An account with this email already exists.'
            in response.content.decode()
    )

@pytest.mark.django_db
def test_registration_normalizes_email_before_saving(client):
    response = client.post(
        reverse("register"),
        {
            'username': 'normalized_user',
            'email': 'Normalized@Example.COM  ',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        },
    )
    assert response.status_code == 302

    user = User.objects.get(username="normalized_user")

    assert user.email == 'normalized@example.com'
