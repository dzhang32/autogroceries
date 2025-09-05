from abc import ABC, abstractmethod
from pathlib import Path

from playwright.sync_api import Page, Playwright

from autogroceries.logging import setup_logger


class Shopper(ABC):
    USER_AGENT = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/17.6 Safari/605.1.15"
    )

    def __init__(
        self, username: str, password: str, log_path: Path | None = None
    ) -> None:
        self.username = username
        self.password = password
        self.logger = setup_logger(log_path)

    def setup_page(self, p: Playwright) -> Page:
        # Try to avoid bot detection.
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        # Set context to emulate a real user with rotating user agent.
        context = browser.new_context(
            user_agent=self.USER_AGENT,
            viewport={"width": 1366, "height": 768},
            locale="en-GB",
            timezone_id="Europe/London",
        )

        return context.new_page()

    @abstractmethod
    def shop(self, ingredients: dict[str, int]) -> None:
        pass
