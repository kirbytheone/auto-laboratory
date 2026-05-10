from pathlib import Path

from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class ModalPage(BasePage):

    BASE_DIR = Path(__file__).resolve().parent.parent
    URL = (BASE_DIR / "test_pages" / "modal.html").as_uri()

    OPEN_MODAL_BUTTON = (By.ID, "open-modal")
    MODAL = (By.ID, "modal")
    CONFIRM_BUTTON = (By.ID, "confirm-btn")

    def open_page(self):
        self.open(self.URL)

    def open_modal(self):
        self.click(self.OPEN_MODAL_BUTTON)

    def is_modal_visible(self):
        return self.find_element(self.MODAL).is_displayed()

    def is_modal_displayed(self):
        modal = self.driver.find_element(*self.MODAL)
        return modal.is_displayed()

    def click_confirm(self):
        self.click(self.CONFIRM_BUTTON)
