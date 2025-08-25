from playwright.sync_api import TimeoutError, sync_playwright


class SainsburysShopper:
    URL = "https://www.sainsburys.co.uk"

    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password

    def shop(self) -> None:
        with sync_playwright() as p:
            # TODO: refactor this out into ABC.
            browser = p.chromium.launch(headless=False)

            self.page = browser.new_page()
            self.page.goto(self.URL)
            self._handle_cookies()

            self._go_to_login()
            self._handle_cookies()

            self._login()

    def _go_to_login(self) -> None:
        self.page.click("text=Log in")
        self.page.click("text=Groceries account")

    def _handle_cookies(self, timeout: int = 3000) -> None:
        # Wait 3 seconds for the cookies to load.
        try:
            button_selector = "button:has-text('Continue without accepting')"
            self.page.wait_for_selector(button_selector, timeout=timeout)
            self.page.click(button_selector)
        except TimeoutError:
            # TODO: add logging.
            pass

    def _login(self) -> None:
        self.page.fill("#username", self.username)
        self.page.fill("#password", self.password)
        self.page.click("button:has-text('Log in')")
