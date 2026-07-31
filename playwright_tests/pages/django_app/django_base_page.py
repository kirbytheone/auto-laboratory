from playwright.sync_api import Page


class DjangoBasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip('/')

    def open_path(self, path: str) -> None:
        normalized_path = path if path.startswith('/') else f"/{path}"
        self.page.goto(f"{self.base_url}{normalized_path}")
