from playwright.sync_api import sync_playwright


class SainsburysShopper:
    URL = "https://www.sainsburys.co.uk"

    def shop(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.goto(self.URL)
            browser.close()