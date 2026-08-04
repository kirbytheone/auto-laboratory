import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PLAYWRIGHT_TESTS_ROOT = PROJECT_ROOT / 'playwright_tests'

PLAYWRIGHT_REPORTS_ROOT = PROJECT_ROOT / "playwright-report"
PRACTICE_REPORTS_DIR = PLAYWRIGHT_REPORTS_ROOT / "practice"
DJANGO_REPORTS_DIR = PLAYWRIGHT_REPORTS_ROOT / "django_app"

PLAYWRIGHT_DOWNLOADS_ROOT = PROJECT_ROOT / "playwright-downloads"
PRACTICE_DOWNLOADS_DIR = PLAYWRIGHT_DOWNLOADS_ROOT / "practice"
DJANGO_DOWNLOADS_DIR = PLAYWRIGHT_DOWNLOADS_ROOT / "django_app"

PLAYWRIGHT_DATA_ROOT = PLAYWRIGHT_TESTS_ROOT / 'data'
PRACTICE_DATA_DIR = PLAYWRIGHT_DATA_ROOT / 'practice'
DJANGO_DATA_DIR = PLAYWRIGHT_DATA_ROOT / 'django_app'

BASE_URL = os.getenv(
    "PLAYWRIGHT_BASE_URL",
    "http://127.0.0.1:8000",
)

TEST_USERNAME = os.getenv('PLAYWRIGHT_TEST_USERNAME')
TEST_PASSWORD = os.getenv('PLAYWRIGHT_TEST_PASSWORD')

TEST_ARTIFACTS = {
    'practice': {
        'reports': PRACTICE_REPORTS_DIR,
        'downloads': PRACTICE_DOWNLOADS_DIR,
        'data': PRACTICE_DATA_DIR,
    },
    'django_app': {
        'reports': DJANGO_REPORTS_DIR,
        'downloads': DJANGO_DOWNLOADS_DIR,
        'data': DJANGO_DATA_DIR,
    },
}

for directory in (
    PRACTICE_REPORTS_DIR,
    DJANGO_REPORTS_DIR,
    PRACTICE_DOWNLOADS_DIR,
    DJANGO_DOWNLOADS_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)

def require_test_credentials() -> tuple[str, str]:
    if not TEST_USERNAME or not TEST_PASSWORD:
        raise RuntimeError(
            'PLAYWRIGHT_TEST_USERNAME and '
            'PLAYWRIGHT_TEST_PASSWORD must be configured'
        )
    return TEST_USERNAME, TEST_PASSWORD


