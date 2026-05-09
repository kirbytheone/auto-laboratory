from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class KeyPressesPage(BasePage):

    URL = "https://the-internet.herokuapp.com/key_presses"

    INPUT_FIELD = (By.ID, "target")
    RESULT_TEXT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def press_key(self, key):
        input_field = self.find_element(self.INPUT_FIELD)
        input_field.click()
        input_field.send_keys(key)

    def get_result_text(self):
        return self.get_text(self.RESULT_TEXT)
