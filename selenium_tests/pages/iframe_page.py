from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class IFramePage(BasePage):

    URL = "https://the-internet.herokuapp.com/iframe"

    IFRAME = (By.ID, "mce_0_ifr")
    TEXT_AREA = (By.ID, "tinymce")

    def open_page(self):
        self.open(self.URL)

    def switch_to_iframe(self):
        iframe = self.find_element(self.IFRAME)
        self.driver.switch_to.frame(iframe)

    def switch_to_default_page(self):
        self.driver.switch_to.default_content()

    def type_text_inside_iframe(self, text: str):
        text_area = self.find_element(self.TEXT_AREA)

        text_area.clear()
        text_area.send_keys(text)

    def get_text_inside_iframe(self):
        return self.get_text(self.TEXT_AREA)
