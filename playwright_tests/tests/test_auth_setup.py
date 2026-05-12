from pathlib import Path
from playwright_tests.pages.login_page import LoginPage


AUTH_STATE_PATH = Path(__file__).resolve().parent.parent / 'auth' / 'auth_state.json'

def test_save_auth_state(browser):
    context = browser.new_context()
    page = context.new_page()

    login_page = LoginPage(page)
    login_page.open_page()
    login_page.login('tomsmith', 'SuperSecretPassword!')

    context.storage_state(path=str(AUTH_STATE_PATH))

    context.close()
