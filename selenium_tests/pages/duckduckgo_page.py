from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium_tests.pages.base_page import BasePage

class DuckDuckPage(BasePage):

    URL = "https://duckduckgo.com"
    SEARCH_INPUT = (By.NAME, "q")

    def open_page(self):
        self.open(self.URL)

    def search(self, text: str):
        self.type_text(self.SEARCH_INPUT, text)
        self.find_element(self.SEARCH_INPUT).send_keys(Keys.ENTER)

    def get_page_title(self):
        return self.get_title()