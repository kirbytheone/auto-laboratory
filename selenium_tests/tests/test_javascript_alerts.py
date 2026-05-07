from selenium_tests.pages.javascript_alerts_page import JavascriptAlertsPage

def test_accept_javascript_alert(driver):
    page = JavascriptAlertsPage(driver)
    page.open_page()
    page.trigger_alert()

    page.accept_alert()

    assert page.get_result_text() == 'You successfully clicked an alert'
