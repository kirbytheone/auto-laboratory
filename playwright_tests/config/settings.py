import os

from dotenv import load_dotenv

load_dotenv()


BASE_URL = os.getenv(
    "PLAYWRIGHT_BASE_URL",
    "http://127.0.0.1:8000",
)

TEST_USERNAME = os.getenv('PLAYWRIGHT_TEST_USERNAME')
TEST_PASSWORD = os.getenv('PLAYWRIGHT_TEST_PASSWORD')

def require_test_credentials() -> tuple[str, str]:
    if not TEST_USERNAME or not TEST_PASSWORD:
        raise RuntimeError(
            'PLAYWRIGHT_TEST_USERNAME and '
            'PLAYWRIGHT_TEST_PASSWORD must be configured'
        )
    return TEST_USERNAME, TEST_PASSWORD


