import pytest

from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_user_can_register(client):
    response = client.post(
        reverse("register"),
        {
            "username": "newuser",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        },
    )

    assert response.status_code == 302
    assert User.objects.filter(username="newuser").exists()

@pytest.mark.django_db
def test_registered_password_is_hashed(client):
    raw_password = "StrongPass123!"

    client.post(
        reverse("register"),
        {
            "username": "secureuser",
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
