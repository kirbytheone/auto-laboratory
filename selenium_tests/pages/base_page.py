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

    def find_elements(self, locator: tuple[str, str]):
        return self.wait.until(lambda driver: driver.find_elements(*locator))

    def wait_until_clickable(self, locator: tuple[str, str]):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str]):
        self.find_element(locator).click()

    def type_text(self, locator: tuple[str, str], text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]):
        return self.find_element(locator).text

    def wait_for_text_in_element(self, locator: tuple[str, str], text: str):
        self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def get_title(self):
        return self.driver.title

    def wait_for_title_content(self, text: str):
        self.wait.until(lambda driver: text.lower() in driver.title.lower())

    def wait_until_url_contains(self, text: str):
        self.wait.until(lambda driver: text in driver.current_url)

    def wait_until_element_disappears(self, locator: tuple[str, str]):
        self.wait.until(lambda driver: not driver.find_element(*locator).is_displayed())
