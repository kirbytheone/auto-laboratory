from pathlib import Path

import pytest

from playwright_tests.config.settings import TEST_ARTIFACTS


def get_test_type(request: pytest.FixtureRequest) -> str:
    if request.node.get_closest_marker("django_app"):
        return 'django_app'
    if request.node.get_closest_marker('practice'):
        return 'practice'
    raise RuntimeError(
        f'Playwright test "{request.node.nodeid}" must have either '
        f'"practice" or "django_app" marker!'
    )

def get_test_artifacts(request: pytest.FixtureRequest) -> dict[str, Path]:
    test_type = get_test_type(request)
    return TEST_ARTIFACTS[test_type]


@pytest.fixture
def page(browser, request):
    context = browser.new_context()

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    page = context.new_page()

    yield page

    artifacts = get_test_artifacts(request)

    if request.node.report_call.failed:
        traceback_path = artifacts['reports'] / f'{request.node.name}.zip'
        context.tracing.stop(path=str(traceback_path))
    else:
        context.tracing.stop()

    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    setattr(item, "report_" + report.when, report)
