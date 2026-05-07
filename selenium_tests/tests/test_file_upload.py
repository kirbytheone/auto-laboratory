from pathlib import Path

from selenium_tests.pages.file_upload_page import FileUploadPage


def test_file_upload(driver):
    page = FileUploadPage(driver)

    file_path = Path("selenium_tests/test_data/sample.txt").resolve()

    page.open_page()
    page.upload_file(str(file_path))
    page.click_upload_file()

    assert page.get_uploaded_filename() == "sample.txt"
