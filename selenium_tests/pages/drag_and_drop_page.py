from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium_tests.pages.base_page import BasePage


class DragAndDropPage(BasePage):

    URL = "https://the-internet.herokuapp.com/drag_and_drop"

    COLUMN_A = (By.ID, "column-a")
    COLUMN_B = (By.ID, "column-b")

    def open_page(self):
        self.open(self.URL)

    def drag_a_to_b(self):
        source = self.find_element(self.COLUMN_A)
        target = self.find_element(self.COLUMN_B)

        ActionChains(self.driver).drag_and_drop(source, target).perform()

    def get_column_a_text(self):
        return self.get_text(self.COLUMN_A)

    def get_column_b_text(self):
        return self.get_text(self.COLUMN_B)
