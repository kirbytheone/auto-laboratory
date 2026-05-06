from selenium_tests.pages.duckduckgo_page import DuckDuckPage


def test_search_title(driver):
    google_page = DuckDuckPage(driver)

    google_page.open_page()
    google_page.search('pytest selenium')

    google_page.wait_for_title_content('pytest selenium')

    assert 'pytest selenium' in google_page.get_page_title().lower()
