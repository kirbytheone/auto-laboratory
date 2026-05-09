from selenium_tests.pages.hovers_page import HoversPage


def test_hover_reveals_caption(driver):
    page = HoversPage(driver)

    page.open_page()
    page.hover_over_user(0)

    assert "name: user1" in page.get_caption_text(0).lower()
