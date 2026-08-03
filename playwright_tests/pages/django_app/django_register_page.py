from playwright.sync_api import Page

from playwright_tests.pages.django_app.django_base_page import DjangoBasePage


class DjangoRegisterPage(DjangoBasePage):
    PATH = '/accounts/register/'

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        self.username_input = page.get_by_label('Username')
        self.password_input = page.get_by_label('Password:')
        self.password_confirmation_input = page.get_by_label('Password confirmation')
        self.email_input = page.get_by_label('Email')
        self.register_button = page.get_by_role('button', name='Register')

        self.duplicate_username_error = page.get_by_text(
            'A user with that username already exists.'
        )
        self.duplicate_email_error = page.get_by_text(
            'An account with this email already exists.'
        )
        self.password_mismatch_error = page.get_by_text(
            'The two password fields didn’t match.'
        )
        self.weak_password_error = page.get_by_text(
            'This password is too common.'
        )

    def open(self) -> None:
        self.open_path(self.PATH)

    def register(self, username: str, email: str, password: str,
                 password_confirmation: str) -> None:
        self.username_input.fill(username)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.password_confirmation_input.fill(password_confirmation)
        self.register_button.click()







