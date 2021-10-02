from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


class Shopper():
    def __init__(self, url):
        self._url = url
        self._webdriver = webdriver
        self._webdriver_manager = ChromeDriverManager()
        self._driver = None

    @property
    def url(self):
        return self._url

    @property
    def webdriver(self):
        return self._webdriver

    @webdriver.setter
    def webdriver(self, value):
        self._webdriver = value

    @property
    def webdriver_manager(self):
        return self._webdriver_manager

    @property
    def driver(self):
        return self._driver

    def open_driver(self):
        driver = self.webdriver.Chrome(self.webdriver_manager.install())
        self._driver = driver

    def open_url(self):
        self._check_driver_is_not_none()
        self.driver.get(self.url)

    def close_driver(self):
        self._driver.close()

    def _check_driver_is_not_none(self):
        if self.driver is None:
            raise ValueError("driver has not yet been initialised")


if __name__ == "__main__":
    b = Shopper("https://www.sainsburys.co.uk")
    # b.open_driver()
    b.open_site()
    b.close_driver()
