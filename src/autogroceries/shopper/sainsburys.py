from playwright.sync_api import TimeoutError, sync_playwright

from autogroceries.exceptions import TwoFactorAuthenticationRequiredError
from autogroceries.pause import pause
from autogroceries.shopper.base import Shopper


class SainsburysShopper(Shopper):
    URL = "https://www.sainsburys.co.uk"

    def shop(self) -> None:
        with sync_playwright() as p:
            self.page = self.setup_page(p)

            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()
            self._handle_cookies()

            self._login()
            self._check_two_factor()

            self._search_item("milk")

    @pause
    def _handle_cookies(self, timeout: int = 3000) -> None:
        try:
            button_selector = "button:has-text('Continue without accepting')"
            self.page.wait_for_selector(button_selector, timeout=timeout)
            self.page.locator(button_selector).click()
        except TimeoutError:
            # TODO: add logging.
            pass

    @pause
    def _go_to_login(self) -> None:
        self.page.locator("text=Log in").click()
        self.page.locator("text=Groceries account").click()

    @pause
    def _login(self) -> None:
        self.page.type("#username", self.username, delay=100)
        self.page.type("#password", self.password, delay=100)
        self.page.locator("button:has-text('Log in')").click()

    @pause(delay=20)
    def _check_two_factor(self) -> None:
        try:
            self.page.wait_for_selector(
                "text=Enter the code sent to your phone", timeout=3000
            )
            raise TwoFactorAuthenticationRequiredError(
                "Two-factor authentication required. Please login to your account "
                "manually then rerun autogroceries."
            )
        except TimeoutError:
            # TODO: add logging.
            pass

    @pause
    def _search_item(self, item: str) -> None:
        self.page.locator("#search-bar-input").fill(item)
        self.page.locator(".search-bar__button").click()
        products = self.page.locator("div.ln-c-card.pt.pt-card")
        for product in products:
            print(product.text_content())
