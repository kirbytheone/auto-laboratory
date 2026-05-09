from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class TablesPage(BasePage):

    URL = "https://the-internet.herokuapp.com/tables"

    TABLE_1_ROWS = (By.CSS_SELECTOR, "#table1 tbody tr")

    def open_page(self):
        self.open(self.URL)

    def get_table_rows(self):
        return self.find_elements(self.TABLE_1_ROWS)

    def get_row_texts(self):
        return [row.text for row in self.get_table_rows()]