class BasePage:

    def __init__(self, page):
        self.page = page

    def open(self, url: str):
        self.page.goto(url)

    def click(self, locator: str):
        self.page.locator(locator).click()

    def fill(self, locator: str, text: str):
        self.page.locator(locator).fill(text)

    def get_text(self, locator: str):
        return self.page.locator(locator).text_content()

    def get_title(self):
        return self.page.title()
