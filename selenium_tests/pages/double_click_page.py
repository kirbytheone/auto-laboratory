from pathlib import Path

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium_tests.pages.base_page import BasePage


class DoubleClickPage(BasePage):
    BASE_DIR = Path(__file__).resolve().parent.parent
    URL = (BASE_DIR / "test_pages" / "double_click.html").as_uri()

    BUTTON = (By.ID, "double-click-button")
    RESULT_TEXT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def double_click_enable(self):
        button = self.find_element(self.BUTTON)

        ActionChains(self.driver).double_click(button).perform()

    def get_result_text(self):
        return self.get_text(self.RESULT_TEXT)
