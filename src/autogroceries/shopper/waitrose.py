from playwright.sync_api import TimeoutError, sync_playwright

from autogroceries.delay import delay
from autogroceries.shopper.base import Shopper


class WaitroseShopper(Shopper):
    """
    Shops for ingredients at Waitrose.

    __init__ is inherited from the `autogroceries.shopper.base.Shopper` abstract base
    class.
    """

    URL = "https://www.waitrose.com"

    def shop(self, ingredients: dict[str, int]) -> None:
        """
        Shop for ingredients at Waitrose.

        Args:
            ingredients: Keys are the ingredients to add to the basket and values are
                the desired quantity of each ingredient.
        """
        self.logger.info("----- Shopping at Waitrose -----")

        with sync_playwright() as p:
            self.page = self.setup_page(p)

            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()

            self._login()

            for ingredient, n in ingredients.items():
                self._add_ingredient(ingredient, n)

        self.logger.info("----- Done -----")

    @delay
    def _handle_cookies(self) -> None:
        """
        Handle the cookie pop up, which otherwise masks the rest of the page.
        """
        try:
            button_selector = "button[data-testid='reject-all']"
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
        self.page.locator("text=Sign in").click()

    @delay
    def _login(self) -> None:
        """
        Login with the provided username and password.
        """
        self.page.type("#email", self.username, delay=50)
        self.page.type("#password", self.password, delay=50)
        self.page.locator("button#loginSubmit").click()

    @delay
    def _add_ingredient(self, ingredient: str, n: int) -> None:
        """
        Search for and add product to basket matching a provided ingredient.

        Args:
            ingredient: The ingredient you would like to buy.
            n: The desired quantity of the ingredient.
        """
        search_input = self.page.locator("input[data-element='search-term']")
        search_input.type(ingredient, delay=50)
        search_input.press("Enter")

        try:
            # If no product found in 10s, skip this ingredient.
            self.page.wait_for_selector(
                "[data-testid='product-list']",
                state="visible",
                timeout=10000,
            )

            products = self.page.locator('[data-testid="product-pod"]').all()

            selected_product = None
            for i, product in enumerate(products):
                # Only check the first 5 products.
                if i >= 5:
                    break

                # Default to selecting the first product.
                if i == 0:
                    selected_product = product

                # Prefer favourited products.
                # If favourited, product will have a remove (from favourites) button.
                if product.locator("button[data-actiontype='remove']").count() > 0:
                    selected_product = product
                    break

            if selected_product:
                product_name = selected_product.locator(
                    "[data-testid='product-pod-name']"
                ).text_content()
                self.logger.info(f"{n} {ingredient.title()}: {product_name}")

                for i in range(n):
                    if i == 0:
                        selected_product.locator(
                            "button[data-testid='addButton']"
                        ).click(delay=100)
                    else:
                        selected_product.locator(
                            "button[data-testid='trolleyPlusButton']"
                        ).click(delay=100)

        except TimeoutError:
            self.logger.warning(f"{n} {ingredient.title()}: no matching product found")

        search_input.clear()
