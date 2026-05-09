from selenium.webdriver.common.keys import Keys

from selenium_tests.pages.key_presses_page import KeyPressesPage


def test_tab_key(driver):
    page = KeyPressesPage(driver)

    page.open_page()
    page.press_key(Keys.TAB)

    page.wait_for_text_in_element(page.RESULT_TEXT, "You entered: TAB")

    assert page.get_result_text() == "You entered: TAB"
