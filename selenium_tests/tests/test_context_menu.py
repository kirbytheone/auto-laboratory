from selenium_tests.pages.context_menu_page import ContextMenuPage


def test_context_menu(driver):
    page = ContextMenuPage(driver)

    page.open_page()
    page.right_click_hotspot()
    page.accept_alert()
