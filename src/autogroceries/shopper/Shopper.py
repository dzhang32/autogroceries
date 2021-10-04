from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Shopper:
    def __init__(self, url, items, n_items = None):
        self._check_items(items)
        self._check_n_items(items, n_items)

        self._url = url
        self._items = items
        self._n_items = n_items
        self.n_items = self._n_items

        self._webdriver = webdriver
        self._webdriver_manager = ChromeDriverManager()
        self._driver = None

    @property
    def url(self):
        return self._url

    @property
    def items(self):
        return self._items

    @property
    def n_items(self):
        return self._n_items

    @n_items.setter
    def n_items(self, value):
        self._check_n_items(self.items, value)
        if value is None:
            value = [1 for i in range(len(self.items))]

        self._n_items = value

    @property
    def webdriver(self):
        return self._webdriver

    @property
    def webdriver_manager(self):
        return self._webdriver_manager

    @property
    def driver(self):
        return self._driver

    @staticmethod
    def _check_items(items):
        if type(items) is not list:
            raise TypeError("items must be a list")
        elif any(type(n) is not str for n in items):
            raise TypeError("items must be a list of str elements")

    @staticmethod
    def _check_n_items(items, n_items):
        if n_items is not None:

            if type(n_items) is not list:
                raise TypeError("n_items must be a list")
            elif any(type(n) is not int for n in n_items):
                raise TypeError("n_items must be a list of int elements")
            elif len(n_items) != 1 and len(n_items) != len(items):
                raise ValueError("length of n_items and items must be equal")

    def _open_driver(self):
        driver = self.webdriver.Chrome(self.webdriver_manager.install())
        self._driver = driver

    def _open_url(self):
        self._check_driver_is_not_none()
        self.driver.get(self.url)

    def _close_driver(self):
        self._driver.close()

    def _check_driver_is_not_none(self):
        if self.driver is None:
            raise ValueError("driver has not yet been initialised")



if __name__ == "__main__":
    b = Shopper("https://www.sainsburys.co.uk", items = ["something", "else"])
    print(b.items)
    print(b.n_items)