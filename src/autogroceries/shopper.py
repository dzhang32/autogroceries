from playwright.sync_api import TimeoutError, sync_playwright

from autogroceries.exceptions import TwoFactorAuthenticationRequiredError


class SainsburysShopper:
    URL = "https://www.sainsburys.co.uk"

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def shop(self, headless: bool = False) -> None:
        with sync_playwright() as p:
            # TODO: refactor this out into ABC.
            browser = p.chromium.launch(headless=headless)
            self.page = browser.new_page()

            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()
            self._handle_cookies()

            self._login()
            self._check_two_factor()

    def _handle_cookies(self, timeout: int = 3000) -> None:
        try:
            button_selector = "button:has-text('Continue without accepting')"
            self.page.wait_for_selector(button_selector, timeout=timeout)
            self.page.locator(button_selector).click()
        except TimeoutError:
            # TODO: add logging.
            pass

    def _go_to_login(self) -> None:
        self.page.locator("text=Log in").click()
        self.page.locator("text=Groceries account").click()

    def _login(self) -> None:
        self.page.fill("#username", self.username)
        self.page.fill("#password", self.password)
        self.page.locator("button:has-text('Log in')").click()

    def _check_two_factor(self) -> None:
        try:
            self.page.wait_for_selector(
                "text=Enter the code sent to your phone", timeout=3000
            )
        except TimeoutError:
            raise TwoFactorAuthenticationRequiredError(
                "Two-factor authentication required. Please login to your account "
                "manually then rerun autogroceries."
            )

    def _search_item(self, item: str) -> None:
        self.page.fill("#search-bar-input", item)
