from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


SCREENSHOTS_DIR = Path(__file__).resolve().parent.parent / "screenshots"

@pytest.fixture
def driver(request):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options)

    yield driver

    if request.node.rep_call.failed:
        SCREENSHOTS_DIR.mkdir(exist_ok=True)
        test_name = request.node.name
        driver.save_screenshot(str(SCREENSHOTS_DIR / f'{test_name}.png'))

    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    setattr(item, "rep_" + rep.when, rep)
