from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

from selenium_tests.pages.base_page import BasePage


class ContextMenuPage(BasePage):

    URL = "https://the-internet.herokuapp.com/context_menu"

    HOTSPOT = (By.ID, "hot-spot")

    def open_page(self):
        self.open(self.URL)

    def right_click_hotspot(self):
        hotspot = self.find_element(self.HOTSPOT)

        ActionChains(self.driver).context_click(hotspot).perform()

    def accept_alert(self):
        self.driver.switch_to.alert.accept()
