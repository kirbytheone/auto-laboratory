import pytest

from playwright_tests.config.settings import PRACTICE_DATA_DIR


TEST_FILE_PATH = PRACTICE_DATA_DIR / 'upload_file.txt'


@pytest.mark.practice
def test_file_upload(page):
    page.goto("https://the-internet.herokuapp.com/upload")

    page.set_input_files("#file-upload", str(TEST_FILE_PATH))
    page.click("#file-submit")
    uploaded_file_name = page.locator('#uploaded-files').inner_text().strip()

    assert uploaded_file_name == "upload_file.txt"
