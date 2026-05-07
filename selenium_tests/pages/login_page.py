from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class LoginPage(BasePage):

    URL = "https://the-internet.herokuapp.com/login"

    USERNAME_INPUT = (By.ID, "username")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    SUCCESS_MESSAGE = (By.ID, "flash")
    ERROR_MESSAGE = (By.ID, "flash")

    def open_page(self):
        self.open(self.URL)

    def login(self, username: str, password: str):
        self.type_text(self.USERNAME_INPUT, username)
        self.type_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)

    def get_success_message(self):
        return self.find_element(self.SUCCESS_MESSAGE).text

    def get_error_message(self):
        return self.find_element(self.ERROR_MESSAGE).text
    
