import pytest

from playwright_tests.config.settings import PRACTICE_DOWNLOADS_DIR


@pytest.mark.practice
def test_file_download(page):
    page.goto("https://the-internet.herokuapp.com/download")

    with page.expect_download() as download_info:
        page.click("text=some-file.txt")

    downloaded_file = download_info.value

    save_path = PRACTICE_DOWNLOADS_DIR / downloaded_file.suggested_filename

    downloaded_file.save_as(str(save_path))

    assert save_path.exists()
