import pytest
from playwright.sync_api import expect

from playwright_tests.config.settings import BASE_URL, require_test_credentials
from playwright_tests.pages.django_app.django_login_page import DjangoLoginPage


@pytest.mark.django_app
def test_valid_regular_user_login(page):
    username, password = require_test_credentials()
    login_page = DjangoLoginPage(page, BASE_URL)

    login_page.open()
    login_page.login(username, password)

    expect(page).not_to_have_url(f'{BASE_URL}/accounts/login/')
    expect(login_page.tasks_link).to_be_visible()

@pytest.mark.django_app
@pytest.mark.parametrize(
    'username,password',
    [
        ('invalid_user', 'invalid_password'),
        ('admin', 'invalid_password'),
    ],
    ids=[
        'wrong_username',
        'wrong_password',
    ],
)
def test_invalid_login(page, username, password):
    login_page = DjangoLoginPage(page, BASE_URL)

    login_page.open()
    login_page.login(username, password)

    expect(login_page.invalid_credentials_message).to_be_visible()
    expect(login_page.authentication_error).to_contain_text(
        'Please enter a correct username and password.'
    )
    expect(page).to_have_url(f'{BASE_URL}/accounts/login/')
