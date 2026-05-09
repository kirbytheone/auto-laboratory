from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium_tests.pages.base_page import BasePage


class HoversPage(BasePage):

    URL = "https://the-internet.herokuapp.com/hovers"

    USER_IMAGES = (By.CLASS_NAME, "figure")
    USER_CAPTIONS = (By.CLASS_NAME, "figcaption")

    def open_page(self):
        self.open(self.URL)

    def hover_over_user(self, index: int):
        user = self.find_elements(self.USER_IMAGES)[index]

        ActionChains(self.driver).move_to_element(user).perform()

    def get_caption_text(self, index: int):
        captions = self.find_elements(self.USER_CAPTIONS)
        return captions[index].text
