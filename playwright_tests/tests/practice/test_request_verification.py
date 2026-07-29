def test_verify_request_url(page):
    with page.expect_request("**/posts/1") as request_info:
        page.goto("https://jsonplaceholder.typicode.com/posts/1")

    request = request_info.value

    assert request.method == "GET"
    assert "/posts/1" in request.url
