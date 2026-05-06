from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self, url: str):
        self.driver.get(url)

    def find_element(self, locator: tuple[str, str]):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator: tuple[str, str]):
        self.find_element(locator).click()

    def type_text(self, locator: tuple[str, str], text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_title(self):
        return self.driver.title

    def wait_for_title_content(self, text: str):
        self.wait.until(lambda driver: text.lower() in driver.title.lower())
