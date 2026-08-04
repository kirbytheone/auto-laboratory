from playwright.sync_api import Locator, Page

from playwright_tests.pages.django_app.django_base_page import DjangoBasePage


class DjangoTaskListPage(DjangoBasePage):
    PATH = '/tasks/'

    def __init__(self, page: Page, base_url: str):
        super().__init__(page, base_url)

        self.heading = page.get_by_role('heading', name='My Tasks')
        self.create_task_link = page.get_by_role('link', name='Create Task')
        self.logout_button = page.get_by_role('button', name='Log Out')

    def logged_in_as(self, username: str) -> Locator:
        return self.page.get_by_text(f'Logged in as {username}')

    def logout(self) -> None:
        self.logout_button.click()
