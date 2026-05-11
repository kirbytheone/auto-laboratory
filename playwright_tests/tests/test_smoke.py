def test_playwright_smoke(page):
    page.goto("https://the-internet.herokuapp.com")

    assert "The Internet" in page.title()