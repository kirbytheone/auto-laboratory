import pytest
from playwright.sync_api import expect

from playwright_tests.config.settings import BASE_URL
from playwright_tests.data.django_app.user_data import generate_user_data
from playwright_tests.pages.django_app.django_register_page import DjangoRegisterPage
from playwright_tests.pages.django_app.django_task_list_page import DjangoTaskListPage


@pytest.mark.django_app
def test_successful_registration(page):
    user = generate_user_data()

    register_page = DjangoRegisterPage(page, BASE_URL)

    register_page.open()
    register_page.register(
        username=user.username,
        email=user.email,
        password=user.password,
        password_confirmation=user.password,
    )

    task_list_page = DjangoTaskListPage(page, BASE_URL)

    expect(page).to_have_url(f'{BASE_URL}{DjangoTaskListPage.PATH}')
    expect(task_list_page.heading).to_be_visible()
    expect(task_list_page.logged_in_as(user.username)).to_be_visible()
    expect(task_list_page.logout_button).to_be_visible()

@pytest.mark.django_app
def test_registration_with_password_mismatch(page):
    user = generate_user_data()

    register_page = DjangoRegisterPage(page, BASE_URL)

    register_page.open()
    register_page.register(
        username=user.username,
        email=user.email,
        password=user.password,
        password_confirmation='DifferentPassword123!',
    )

    expect(page).to_have_url(
        f'{BASE_URL}{DjangoRegisterPage.PATH}'
    )
    expect(register_page.password_mismatch_error).to_be_visible()

@pytest.mark.django_app
def test_registration_with_duplicate_username(page):
    user = generate_user_data()

    register_page = DjangoRegisterPage(page, BASE_URL)

    register_page.open()
    register_page.register(
        username=user.username,
        email=user.email,
        password=user.password,
        password_confirmation=user.password,
    )

    task_list_page = DjangoTaskListPage(page, BASE_URL)
    expect(task_list_page.heading).to_be_visible()
    task_list_page.logout()

    register_page.open()
    register_page.register(
        username=user.username,
        email=f'other{user.email}',
        password=user.password,
        password_confirmation=user.password,
    )

    expect(page).to_have_url(f'{BASE_URL}{DjangoRegisterPage.PATH}')
    expect(register_page.duplicate_username_error).to_be_visible()

@pytest.mark.django_app
def test_registration_with_duplicate_email(page):
    user = generate_user_data()

    register_page = DjangoRegisterPage(page, BASE_URL)

    register_page.open()
    register_page.register(
        username=user.username,
        email=user.email,
        password=user.password,
        password_confirmation=user.password,
    )

    task_list_page = DjangoTaskListPage(page, BASE_URL)
    expect(task_list_page.heading).to_be_visible()
    task_list_page.logout()

    register_page.open()
    register_page.register(
        username=f'{user.username}_other',
        email=user.email,
        password=user.password,
        password_confirmation=user.password,
    )

    expect(page).to_have_url(f'{BASE_URL}{DjangoRegisterPage.PATH}')
    expect(register_page.duplicate_email_error).to_be_visible()

@pytest.mark.django_app
def test_registration_with_common_password(page):
    user = generate_user_data()
    weak_password = 'password'

    register_page = DjangoRegisterPage(page, BASE_URL)

    register_page.open()
    register_page.register(
        username=user.username,
        email=user.email,
        password=weak_password,
        password_confirmation=weak_password,
    )

    expect(page).to_have_url(f'{BASE_URL}{DjangoRegisterPage.PATH}')
    expect(register_page.weak_password_error).to_be_visible()
