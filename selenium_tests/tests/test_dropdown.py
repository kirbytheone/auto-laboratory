from selenium_tests.pages.dropdown_page import DropdownPage

def test_select_dropdown_option(driver):
    page = DropdownPage(driver)

    page.open_page()
    page.select_by_visible_text("Option 1")

    assert page.get_selected_option_text() == "Option 1"

