import time
from autogroceries.shopper import Shopper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


class SainsburyShopper(Shopper):

    def __init__(self):
        sainsbury_url = "https://www.sainsburys.co.uk"

        super().__init__(sainsbury_url)

    def shop(self, username, password):
        self._open_sainsbury()
        self._accept_cookies()
        self._to_login()
        self._login(username, password)
        self._add_to_cart("tomato")

    def _add_to_cart(self, item):
        search = self.driver.find_element_by_id("search-bar-input")
        search.send_keys(item)
        search = self.driver.find_element_by_xpath(
            "//button[@class='search-bar__button']"
        )
        search.click()

        # adding to the cart defaults to the first item, needs more
        # complexity here
        wait = WebDriverWait(self.driver, 5)
        add = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Add']"))
        )
        add.click()

    def _open_sainsbury(self):
        self.open_driver()
        self.open_url()

        # wait a second for page to load
        time.sleep(1)

    def _accept_cookies(self):
        # wait for few seconds for the cookies box to become clickable
        wait = WebDriverWait(self.driver, 5)
        accept_box = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Accept All Cookies']"))
        )
        accept_box.click()

    def _to_login(self):
        login = self.driver.find_element_by_xpath("//span[text()='Log in']")
        login.click()
        groceries = self.driver.find_element_by_xpath(
            "//a[text()='Groceries account']"
        )
        groceries.click()

    def _login(self, username, password):
        self.accept_cookies()

        # enter UN and PW
        un = self.driver.find_element_by_id("username")
        un.send_keys(username)
        pw = self.driver.find_element_by_id("password")
        pw.send_keys(password)

        login = self.driver.find_element_by_xpath("//button[text()='Log in']")
        login.click()

        # two-step auth via email... need to think about how best
        # to get around this - some potential for automation
        # currently wait for 2 mins and enter manually
        try:
            wait = WebDriverWait(self.driver, 5)
            cont = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Continue']"))
            )
            cont.click()
        except:
            pass


if __name__ == "__main__":
    with open("/Users/david_zhang/dz_home/work/data_sci/autogroceries/credentials.txt") as file:
        credentials = file.readlines()
    sb = SainsburyShopper()
    sb.shop(credentials[0], credentials[1])