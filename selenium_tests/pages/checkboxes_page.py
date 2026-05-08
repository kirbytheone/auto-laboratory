from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class CheckboxesPage(BasePage):

    URL = "https://the-internet.herokuapp.com/checkboxes"

    CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")

    def open_page(self):
        self.open(self.URL)

    def get_checkboxes(self):
        return self.find_elements(self.CHECKBOXES)

    def check_checkbox(self, index: int):
        checkbox = self.get_checkboxes()[index]

        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_checkbox(self, index: int):
        checkbox = self.get_checkboxes()[index]

        if checkbox.is_selected():
            checkbox.click()

    def is_checkbox_selected(self, index: int):
        return self.get_checkboxes()[index].is_selected()