from playwright.sync_api import expect


def test_mock_page(page):
    page.route(
        "https://jsonplaceholder.typicode.com/posts/1",
        lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body='{"id": 1, "title": "Mocked title"}',
        ),
    )

    page.goto("https://jsonplaceholder.typicode.com/posts/1")

    expect(page.locator("body")).to_contain_text("Mocked title")
