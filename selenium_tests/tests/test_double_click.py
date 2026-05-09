from selenium_tests.pages.double_click_page import DoubleClickPage


def test_double_click(driver):
    page = DoubleClickPage(driver)

    page.open_page()
    page.double_click_enable()

    assert page.get_result_text() == 'Double clicked!'