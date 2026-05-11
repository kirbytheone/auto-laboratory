from selenium_tests.pages.checkboxes_page import CheckboxesPage

def test_check_first_checkbox(driver):
    page = CheckboxesPage(driver)

    page.open_page()
    page.check_checkbox(0)

    assert False

    assert page.is_checkbox_selected(0)

def test_uncheck_second_checkbox(driver):
    page = CheckboxesPage(driver)

    page.open_page()
    page.uncheck_checkbox(1)

    assert not page.is_checkbox_selected(1)
