import pytest

from django.contrib.auth.models import User
from django.test import override_settings

from rest_framework.test import APIClient

from tasks.models import Task


@pytest.fixture
def temporary_media_root(tmp_path):
    with override_settings(MEDIA_ROOT=tmp_path):
        yield tmp_path

@pytest.fixture
def create_user():
    def _create_user(
            username="testuser",
            password="testpass123",
            is_staff=False,
            is_superuser=False,
    ):
        return User.objects.create_user(
            username=username,
            password=password,
            is_staff=is_staff,
            is_superuser=is_superuser,
        )
    return _create_user

@pytest.fixture
def create_task():
    def _create_task(
            owner,
            title="Test Task",
            description="Test Description",
            status="todo",
            priority="medium",
            due_date=None,
    ):

        return Task.objects.create(
            owner=owner,
            title=title,
            description=description,
            status=status,
            priority=priority,
            due_date=due_date,
        )
    return _create_task

@pytest.fixture
def api_client():
    return APIClient()
