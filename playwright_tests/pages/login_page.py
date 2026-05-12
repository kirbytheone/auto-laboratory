from playwright_tests.pages.base_page import BasePage


class LoginPage(BasePage):

    URL = "https://the-internet.herokuapp.com/login"

    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "button[type='submit']"
    FLASH_MESSAGE = "#flash"

    def open_page(self):
        self.open(self.URL)

    def login(self, username: str, password: str):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def flash_message(self):
        return self.get_locator(self.FLASH_MESSAGE)

    def get_flash_message(self):
        return self.get_text(self.FLASH_MESSAGE)
