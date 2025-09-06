from playwright.sync_api import TimeoutError, sync_playwright

from autogroceries.delay import delay
from autogroceries.exceptions import TwoFactorAuthenticationRequiredError
from autogroceries.shopper.base import Shopper


class SainsburysShopper(Shopper):
    """
    Shops for ingredients at Sainsbury's.

    __init__ is inherited from the `autogroceries.shopper.base.Shopper` abstract base
    class.
    """

    URL = "https://www.sainsburys.co.uk"

    def shop(self, ingredients: dict[str, int]) -> None:
        """
        Shop for ingredients at Sainsbury's.

        Args:
            ingredients: Keys are the ingredients to add to the basket and values are
                the desired quantity of each ingredient.
        """
        self.logger.info("----- Shopping at Sainsbury's -----")

        with sync_playwright() as p:
            self.page = self.setup_page(p)

            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()
            self._handle_cookies()

            self._login()
            self._check_two_factor()
            self._check_empty_basket()

            for ingredient, n in ingredients.items():
                self._add_ingredient(ingredient, n)

        self.logger.info("----- Done -----")

    @delay
    def _handle_cookies(self) -> None:
        """
        Handle the cookie pop up, which otherwise masks the rest of the page.
        """
        try:
            button_selector = "button:has-text('Continue without accepting')"
            self.page.wait_for_selector(button_selector, timeout=3000)
            self.page.locator(button_selector).click()
            self.logger.info("Rejecting cookies")
        except TimeoutError:
            self.logger.info("No cookies popup found")
            pass

    @delay
    def _go_to_login(self) -> None:
        """
        Go to the login page.
        """
        self.page.locator("text=Log in").click()
        self.page.locator("text=Groceries account").click()

    @delay
    def _login(self) -> None:
        """
        Login with the provided username and password.
        """
        self.page.type("#username", self.username, delay=50)
        self.page.type("#password", self.password, delay=50)
        self.page.locator("button:has-text('Log in')").click()

    @delay
    def _check_two_factor(self) -> None:
        """
        Check if two-factor authentication is required.

        Raises:
            TwoFactorAuthenticationRequiredError: If required, user must manually login
                to their account first.
        """
        try:
            self.page.wait_for_selector(
                "text=Enter the code sent to your phone", timeout=3000
            )
            raise TwoFactorAuthenticationRequiredError(
                "Two-factor authentication required. Please login to your account "
                "manually then rerun autogroceries."
            )
        except TimeoutError:
            self.logger.info("Login successful (no two-factor authentication required)")
            pass

    @delay
    def _check_empty_basket(self) -> None:
        """
        Check if basket is initially empty.

        If basket not empty, autogroceries will error if it tries to add a product that
        is already in the basket.
        """
        if self.page.locator(".header-trolley ").count() > 0:
            self.logger.warning(
                "Basket is not initially empty. This may cause issues when adding products."
            )

    @delay
    def _add_ingredient(self, ingredient: str, n: int) -> None:
        """
        Search for and add product to basket matching a provided ingredient.

        Args:
            ingredient: The ingredient you would like to buy.
            n: The desired quantity of the ingredient.
        """
        # There are two search inputs on the same page, use the first.
        search_input = self.page.locator("#search-bar-input").first
        search_input.type(ingredient, delay=50)
        self.page.locator(".search-bar__button").first.click()

        try:
            # If no product found in 10s, skip this ingredient.
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

                # Prefer favourited products.
                if (
                    product.locator("button[data-testid='favourite-icon-full']").count()
                    > 0
                ):
                    selected_product = product
                    break

            if selected_product:
                product_name = selected_product.locator(
                    ".pt__info__description"
                ).text_content()
                self.logger.info(f"{n} {ingredient.title()}: {product_name}")

                for i in range(n):
                    if i == 0:
                        selected_product.locator(
                            "button[data-testid='add-button']"
                        ).click(delay=100)
                    else:
                        selected_product.locator(
                            "button[data-testid='pt-button-inc']"
                        ).click(delay=100)

        except TimeoutError:
            self.logger.warning(f"{n} {ingredient.title()}: no matching product found")

        search_input.clear()
