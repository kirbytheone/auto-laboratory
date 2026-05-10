from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class DynamicControlsPage(BasePage):

    URL = "https://the-internet.herokuapp.com/dynamic_controls"

    ENABLE_BUTTON = (By.XPATH, "//button[normalize-space()='Enable']")
    DISABLE_BUTTON = (By.XPATH, "//button[normalize-space()='Disable']")
    INPUT_FIELD = (By.CSS_SELECTOR, "#input-example input")
    TOGGLE_INPUT_BUTTON = (By.CSS_SELECTOR, "#input-example button")
    MESSAGE = (By.ID, "message")

    def open_page(self):
        self.open(self.URL)

    def click_toggle_input(self):
        self.click(self.TOGGLE_INPUT_BUTTON)

    def wait_until_input_enabled(self):
        self.wait.until(lambda driver: driver.find_element(*self.INPUT_FIELD).is_enabled())

    def wait_until_input_disabled(self):
        self.wait.until(lambda driver: not driver.find_element(*self.INPUT_FIELD).is_enabled())

    def is_input_enabled(self):
        return self.find_element(self.INPUT_FIELD).is_enabled()

    def get_message(self):
        return self.get_text(self.MESSAGE)
