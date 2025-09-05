from playwright.sync_api import TimeoutError, sync_playwright

from autogroceries.exceptions import TwoFactorAuthenticationRequiredError
from autogroceries.pause import pause
from autogroceries.shopper.base import Shopper


class SainsburysShopper(Shopper):
    URL = "https://www.sainsburys.co.uk"

    def shop(self, ingredients: dict[str, int]) -> None:
        """
        Assumes that the basket is initially empty.
        """
        with sync_playwright() as p:
            self.page = self.setup_page(p)

            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()
            self._handle_cookies()

            self._login()
            self._check_two_factor()

            for ingredient, n in ingredients.items():
                self._add_product(ingredient, n)

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
        self.page.type("#username", self.username, delay=50)
        self.page.type("#password", self.password, delay=50)
        self.page.locator("button:has-text('Log in')").click()

    @pause
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
    def _add_product(self, ingredient: str, n: int) -> None:
        # There are two search inputs on the same page, use the first.
        search_input = self.page.locator("#search-bar-input").first
        search_input.type(ingredient, delay=50)
        self.page.locator(".search-bar__button").first.click()

        self.page.wait_for_selector(
            ".product-tile-row",
            state="visible",
            timeout=10000,
        )

        products = self.page.locator('[data-testid^="product-tile-"]').all()

        selected_product = None
        for i, product in enumerate(products):
            # Only check the first 5 products.
            if i >= 5:
                break

            # Default to selecting the first product.
            if i == 0:
                selected_product = product

            if product.locator("button[data-testid='favourite-icon-full']").count() > 0:
                selected_product = product
                break

        if selected_product:
            for i in range(n):
                if i == 0:
                    selected_product.locator("button[data-testid='add-button']").click(
                        delay=100
                    )
                else:
                    selected_product.locator(
                        "button[data-testid='pt-button-inc']"
                    ).click(delay=100)

        search_input.clear()
