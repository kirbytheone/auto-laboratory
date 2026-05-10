from selenium_tests.pages.modal_page import ModalPage


def test_modal_open(driver):
    page = ModalPage(driver)

    page.open_page()

    assert not page.is_modal_displayed()

    page.open_modal()

    assert page.is_modal_displayed()
