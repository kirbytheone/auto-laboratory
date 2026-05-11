def test_add_and_read_cookies(driver):
    driver.get("https://the-internet.herokuapp.com")

    driver.add_cookie({
        'name': "test_cookie",
        'value': "selenium_cookie_value"
    })

    cookie = driver.get_cookie("test_cookie")

    assert cookie["name"] == "test_cookie"
    assert cookie["value"] == "selenium_cookie_value"
