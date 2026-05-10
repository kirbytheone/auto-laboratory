from selenium_tests.pages.dynamic_controls_page import DynamicControlsPage


# def test_enable_input_field(driver):
#     page = DynamicControlsPage(driver)
#
#     page.open_page()
#
#     assert not page.is_input_enabled()
#
#     page.click_enable()
#     page.wait_until_input_enabled()
#
#     assert page.is_input_enabled()
#     assert "It's enabled!" in page.get_message()

def test_disable_input_field(driver):
    page = DynamicControlsPage(driver)

    page.open_page()

    assert not page.is_input_enabled()

    page.click_toggle_input()
    page.wait_until_input_enabled()

    assert page.is_input_enabled()
    assert "It's enabled!" in page.get_message()

    page.click_toggle_input()
    page.wait_until_input_disabled()

    assert not page.is_input_enabled()
    assert "It's disabled!" in page.get_message()


















