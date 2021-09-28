class Browser():
    def __init__(self, url, driver):
        self._driver = driver
        self._url = url

    @property
    def driver(self):
        return self._driver

    @property
    def url(self):
        return self._url
