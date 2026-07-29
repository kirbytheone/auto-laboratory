def test__multiple_contexts(browser):
    context_1 = browser.new_context()
    context_2 = browser.new_context()

    page_1 = browser.new_page()
    page_2 = browser.new_page()

    page_1.goto("https://the-internet.herokuapp.com")
    page_2.goto("https://the-internet.herokuapp.com")

    assert "The Internet" in page_1.title()
    assert "The Internet" in page_2.title()

    context_1.close()
    context_2.close()
