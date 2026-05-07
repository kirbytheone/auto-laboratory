from selenium_tests.pages.login_page import LoginPage

def test_login_success(driver):
    page = LoginPage(driver)

    page.open_page()
    page.login('tomsmith', 'SuperSecretPassword!')

    message = page.get_success_message()

    assert 'You logged into a secure area!' in message

def test_invalid_login(driver):
    page = LoginPage(driver)

    page.open_page()
    page.login('tomsmith', 'Wrong Password!')

    message = page.get_error_message()

    assert 'Your password is invalid!' in message
