from selenium import webdriver


class Browser():
    def __init__(self, url, driver):
        self._driver = driver

    @property
    def driver(self):
        return self._driver

    @property
    def url(self):
        return self._url


class SainsburyBrowser(Browser):
    def __init__(self):

        self._url = "https://www.sainsburys.co.uk"

    @property
    def url(self):
        return self._url







