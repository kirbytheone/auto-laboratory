from selenium.webdriver.common.by import By

from selenium_tests.pages.base_page import BasePage


class FileUploadPage(BasePage):

    URL = "https://the-internet.herokuapp.com/upload"

    FILE_INPUT = (By.ID, 'file-upload')
    UPLOAD_BUTTON = (By.ID, 'file-submit')
    UPLOADED_FILE = (By.ID, 'uploaded-files')

    def open_page(self):
        self.open(self.URL)

    def upload_file(self, file_path: str):
        self.find_element(self.FILE_INPUT).send_keys(file_path)

    def click_upload_file(self):
        self.click(self.UPLOAD_BUTTON)

    def get_uploaded_filename(self):
        return self.get_text(self.UPLOADED_FILE)
