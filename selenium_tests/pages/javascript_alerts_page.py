from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class JavascriptAlertsPage(BasePage):

    URL = "https://the-internet.herokuapp.com/javascript_alerts"

    JS_ALERT_BUTTON = (By.XPATH, "//button[text()='Click for JS Alert']")
    RESULT_TEXT = (By.ID, "result")

    def open_page(self):
        self.open(self.URL)

    def trigger_alert(self):
        self.click(self.JS_ALERT_BUTTON)

    def accept_alert(self):
        alert = self.driver.switch_to.alert
        alert.accept()

    def get_result_text(self):
        return self.get_text(self.RESULT_TEXT)
