import pytest
from playwright.sync_api import expect

from playwright_tests.config.settings import BASE_URL, require_test_credentials
from playwright_tests.pages.django_app.django_login_page import DjangoLoginPage
from playwright_tests.pages.django_app.django_task_list_page import DjangoTaskListPage


@pytest.mark.django_app
def test_valid_regular_user_login(page):
    # TODO:
    # Replace environment-based login setup with
    # generated test users once backend/API fixtures
    # are introduced.
    username, password = require_test_credentials()
    login_page = DjangoLoginPage(page, BASE_URL)

    login_page.open()
    login_page.login(username, password)

    task_list_page = DjangoTaskListPage(page, BASE_URL)

    expect(page).to_have_url(f'{BASE_URL}{DjangoTaskListPage.PATH}')
    expect(task_list_page.current_user()).to_have_text(username)
    expect(task_list_page.logout_button).to_be_visible()

@pytest.mark.django_app
def test_login_with_invalid_username(page):
    login_page = DjangoLoginPage(page, BASE_URL)

    login_page.open()
    login_page.login(username='invalid_user', password='invalid_password')

    expect(login_page.invalid_credentials_message).to_be_visible()
    expect(login_page.authentication_error).to_contain_text(
        'Please enter a correct username and password.'
    )
    expect(page).to_have_url(f'{BASE_URL}/accounts/login/')

@pytest.mark.django_app
def test_login_with_wrong_password(page):
    username, _ = require_test_credentials()
    login_page = DjangoLoginPage(page, BASE_URL)

    login_page.open()
    login_page.login(username=username, password='invalid_password')

    expect(login_page.invalid_credentials_message).to_be_visible()
    expect(login_page.authentication_error).to_contain_text(
        'Please enter a correct username and password.'
    )
    expect(page).to_have_url(f'{BASE_URL}/accounts/login/')
