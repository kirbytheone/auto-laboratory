def test_api_get_request(playwright):
    request_context = playwright.request.new_context()

    try:
        response = request_context.get(
            "https://jsonplaceholder.typicode.com/posts/1"
        )

        assert response.status == 200

        body = response.json()
        assert body["id"] == 1
    finally:
        request_context.dispose()
