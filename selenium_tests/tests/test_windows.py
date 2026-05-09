from selenium_tests.pages.windows_page import WindowsPage


def test_switch_to_new_window(driver):
    page = WindowsPage(driver)

    page.open_page()
    page.open_new_window()
    page.switch_to_new_window()

    assert page.get_page_title() == "New Window"

    page.switch_to_main_window()

    assert page.get_page_title() == "The Internet"
