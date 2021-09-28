from autoceries.browser.Browser import Browser


class SainsburyBrowser(Browser):
    def __init__(self, driver):
        sainsbury_url = "https://www.sainsburys.co.uk"

        super().__init__(sainsbury_url, driver)