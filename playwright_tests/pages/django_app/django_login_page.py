from playwright.sync_api import Page

from playwright_tests.pages.django_app.django_base_page import DjangoBasePage


class DjangoLoginPage(DjangoBasePage):
    PATH = '/accounts/login/'

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        self.username_input = page.get_by_label('Username')
        self.password_input = page.get_by_label('Password')
        self.login_button = page.get_by_role('button', name='Log In')

        self.invalid_credentials_message = page.get_by_text(
            'Invalid username or password.'
        )
        self.authentication_error = page.get_by_text(
            'Please enter a correct username and password.'
        )

    def open(self) -> None:
        self.open_path(self.PATH)

    def login(self, username: str, password: str) -> None:
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
