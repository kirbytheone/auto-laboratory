import pytest
from django.test import override_settings


@pytest.fixture
def temporary_media_root(tmp_path):
    with override_settings(MEDIA_ROOT=tmp_path):
        yield tmp_path
