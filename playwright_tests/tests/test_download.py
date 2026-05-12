from playwright_tests.tests.test_file_upload import PROJECT_ROOT_PATH

DOWNLOADS_DIR_PATH = PROJECT_ROOT_PATH / "playwright_downloads"


def test_file_download(page):
    DOWNLOADS_DIR_PATH.mkdir(exist_ok=True)

    page.goto("https://the-internet.herokuapp.com/download")

    with page.expect_download() as download_info:
        page.click("text=some-file.txt")

    downloaded_file = download_info.value

    save_path = DOWNLOADS_DIR_PATH / downloaded_file.suggested_filename

    downloaded_file.save_as(str(save_path))

    assert save_path.exists()
