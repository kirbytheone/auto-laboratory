from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from selenium_tests.pages.base_page import BasePage

class DropdownPage(BasePage):

    URL = 'https://the-internet.herokuapp.com/dropdown'

    DROPDOWN = (By.ID, 'dropdown')

    def open_page(self):
        self.open(self.URL)

    def select_by_visible_text(self, text: str):
        dropdown_element = self.find_element(self.DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_visible_text(text)

    def get_selected_option_text(self):
        dropdown_element = self.find_element(self.DROPDOWN)
        select = Select(dropdown_element)
        return select.first_selected_option.text
