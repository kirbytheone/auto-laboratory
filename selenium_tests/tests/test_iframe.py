from selenium_tests.pages.iframe_page import IFramePage


def test_iframe_text_input(driver):
    page = IFramePage(driver)

    page.open_page()
    page.switch_to_iframe()
    # page.type_text_inside_iframe("Forever and a Day!")
    # assert "Forever and a Day!" in page.get_text_inside_iframe()

    page.wait_for_text_in_element(page.TEXT_AREA, "Your content goes here.")

    assert "Your content goes here." in page.get_text_inside_iframe()

    page.switch_to_default_page()
