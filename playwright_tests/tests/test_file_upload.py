from pathlib import Path


PROJECT_ROOT_PATH = Path(__file__).resolve().parent.parent.parent
TEST_FILE_PATH = PROJECT_ROOT_PATH / 'selenium_tests' / 'test_data' / 'sample.txt'


def test_file_upload(page):
    page.goto("https://the-internet.herokuapp.com/upload")

    page.set_input_files("#file-upload", str(TEST_FILE_PATH))
    page.click("#file-submit")
    uploaded_file_name = page.locator('#uploaded-files').inner_text().strip()

    assert uploaded_file_name == "sample.txt"
