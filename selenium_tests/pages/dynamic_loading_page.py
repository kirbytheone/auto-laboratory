from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class DynamicLoadingPage(BasePage):
     URL = "https://the-internet.herokuapp.com/dynamic_loading/1"

     START_BUTTON = (By.CSS_SELECTOR, '#start button')
     FINISH_TEXT = (By.ID, 'finish')

     def open_page(self):
         self.open(self.URL)

     def click_start(self):
         self.click(self.START_BUTTON)

     def get_finish_text(self):
         return self.get_text(self.FINISH_TEXT)
