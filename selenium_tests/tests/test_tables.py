from selenium_tests.pages.tables_page import TablesPage


def test_table_contains_expected_user(driver):
    page = TablesPage(driver)

    page.open_page()
    rows = page.get_row_texts()

    assert any("Smith" in row for row in rows)
