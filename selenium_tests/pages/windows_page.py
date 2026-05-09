from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class WindowsPage(BasePage):

    URL = "https://the-internet.herokuapp.com/windows"

    CLICK_HERE_LINK = (By.LINK_TEXT, "Click Here")

    def open_page(self):
        self.open(self.URL)

    def open_new_window(self):
        self.click(self.CLICK_HERE_LINK)

    def switch_to_new_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])

    def switch_to_main_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

    def get_page_title(self):
        return self.get_title()
