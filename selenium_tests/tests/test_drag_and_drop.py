from selenium_tests.pages.drag_and_drop_page import DragAndDropPage


def test_drag_and_drop_columns(driver):
    page = DragAndDropPage(driver)

    page.open_page()
    page.drag_a_to_b()

    assert page.get_column_a_text() == "B"
    assert page.get_column_b_text() == "A"
