from selenium_tests.pages.dynamic_loading_page import DynamicLoadingPage


def test_dynamic_loading(driver):
    page = DynamicLoadingPage(driver)

    page.open_page()
    page.click_start()

    page.wait_until_loading_disappears()
    text = page.get_finish_text()

    assert text == 'Hello World!'
