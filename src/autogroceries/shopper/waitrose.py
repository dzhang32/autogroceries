from playwright.sync_api import sync_playwright

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
        self.logger.info("----- Shopping at Waitrose -----")

        with sync_playwright() as p:
            self.page = self.setup_page(p)

            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()

            self._login()
            """
            self._check_two_factor()
            self._check_empty_basket()

            for ingredient, n in ingredients.items():
                self._add_ingredient(ingredient, n)
            """

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
        self.page.locator("text=Sign in").click()

    @delay
    def _login(self) -> None:
        self.page.type("#email", self.username, delay=50)
        self.page.type("#password", self.password, delay=50)
        self.page.locator("button#loginSubmit").click()
