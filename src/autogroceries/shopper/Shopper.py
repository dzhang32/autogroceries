from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Shopper:

    """Automates grocery shopping from a user-inputted URL

    A Shopper object contains methods to open a grocery website and also store
    the details of the food items that are desired to be ordered. Shopper class
    is not intended to be used to created instances, rather be a (virtual) class
    for child Shopper classes to inherit utility methods and attributes from.

    Parameters
    ----------
    url : str
        URL of the grocery store website to order from.
    items : list
        List of items to search for and order.
    n_items : list
        List of equal length to items, determining the number of each item to
        order.
    headless : bool
        Whether to open the Selenium webdriver in headless mode, exists mostly
        for testing.
    """

    def __init__(self, url, items, n_items=None, headless=False):
        self._url = url

        self._check_headless(headless)
        self._headless = headless

        self._check_items(items)
        self._check_n_items(items, n_items)
        self._items = items
        self._n_items = n_items
        self.n_items = self._n_items

        # TODO: refactor the usage of webdriver - should I store entire module?
        self._webdriver = webdriver

        # TODO: add other browsers?
        self._webdriver_manager = ChromeDriverManager()

        # placeholder for setting up a chromedriver
        self._driver = None

    def close_driver(self):
        self.driver.close()

    @property
    def url(self):
        """Return the URL of Shopper"""

        return self._url

    @property
    def headless(self):
        """Return the headless attribute of Shopper"""

        return self._headless

    @headless.setter
    def headless(self, value):
        """Set the headless attribute of Shopper"""

        self._check_headless(value)
        self._headless = value

    @property
    def items(self):
        """Return the items attribute of Shopper"""

        return self._items

    @property
    def n_items(self):
        """Return the n_items attribute of Shopper"""

        return self._n_items

    @n_items.setter
    def n_items(self, value):
        """Set the n_items attribute of Shopper"""

        self._check_n_items(self.items, value)
        if value is None:
            value = [1 for i in range(len(self.items))]

        self._n_items = value

    @property
    def webdriver(self):
        """Return the webdriver attribute of Shopper"""

        return self._webdriver

    @property
    def webdriver_manager(self):
        """Return the webdriver_manager attribute of Shopper"""

        return self._webdriver_manager

    @property
    def driver(self):
        """Return the driver attribute of Shopper"""

        return self._driver

    def _open_driver(self):
        """Open a driver using Selenium (in headless mode if preferred)

        Currently can only use Chrome as the browser.
        """

        if self.headless:
            # TODO: ugly nested call, may rethink - pass options as arg?
            opts = self.webdriver.ChromeOptions()
            opts.add_argument("--headless")

            # need to set user-agent otherwise headless browser is blocked
            # https://intoli.com/blog/making-chrome-headless-undetectable/
            ua = (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                + " (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"
            )
            opts.add_argument(f"user-agent={ua}")
            driver = self.webdriver.Chrome(
                self.webdriver_manager.install(), options=opts
            )
        else:
            driver = self.webdriver.Chrome(self.webdriver_manager.install())

        self._driver = driver

    def _open_url(self):
        """Open the URL attribute in Shopper"""

        self._check_driver_is_not_none()
        self.driver.get(self.url)

    def _check_driver_is_not_none(self):
        """Checks driver has been opened (before trying to open URL)"""

        if self.driver is None:
            raise ValueError("driver has not yet been opened")

    @staticmethod
    def _check_headless(headless):
        """Checks format of headless"""

        if type(headless) is not bool:
            raise TypeError("headless must be a boolean")

    @staticmethod
    def _check_items(items):
        """Check format of items"""

        if type(items) is not list:
            raise TypeError("items must be a list")
        elif any(type(n) is not str for n in items):
            raise TypeError("items must be a list of str elements")

    @staticmethod
    def _check_n_items(items, n_items):
        """Check format of n_items"""

        if n_items is not None:

            if type(n_items) is not list:
                raise TypeError("n_items must be a list")
            elif any(type(n) is not int for n in n_items):
                raise TypeError("n_items must be a list of int elements")
            elif len(n_items) != 1 and len(n_items) != len(items):
                raise ValueError("length of n_items and items must be equal")
