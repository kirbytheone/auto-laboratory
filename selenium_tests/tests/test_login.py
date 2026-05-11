import pytest

from selenium_tests.pages.login_page import LoginPage


@pytest.mark.parametrize(
    "username, password, expected_message",
    [
        ("tomsmith", "wrong_password", "Your password is invalid!"),
        ("wrong_user", "SuperSecretPassword!", "Your username is invalid!"),
    ],
)

def test_invalid_login(driver, username, password, expected_message):
    page = LoginPage(driver)

    page.open_page()
    page.login(username, password)

    message = page.get_error_message()
    assert expected_message in message

def test_login_success(driver):
    page = LoginPage(driver)

    page.open_page()
    page.login('tomsmith', 'SuperSecretPassword!')

    message = page.get_success_message()

    assert 'You logged into a secure area!' in message
