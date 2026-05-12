import pytest

from playwright.sync_api import expect

from playwright_tests.pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("wrong_user", "wrong_password", "Your username is invalid!"),
        ("tomsmith", "wrong_password", "Your password is invalid!"),
    ],
)
def test_invalid_login(page, username, password, expected_message):
    login_page = LoginPage(page)

    login_page.open_page()
    login_page.login(username, password)

    expect(login_page.flash_message()).to_contain_text(expected_message)

