from playwright_tests.pages.login_page import LoginPage


def test_invalid_login(page):
    login_page = LoginPage(page)

    login_page.open_page()
    login_page.login("wrong_user", "wrong_password")

    assert "Your username is invalid!" in login_page.get_flash_message()
