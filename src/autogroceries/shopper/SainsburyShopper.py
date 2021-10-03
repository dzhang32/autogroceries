import time
from autogroceries.shopper import Shopper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys


class SainsburyShopper(Shopper):

    def __init__(self):
        sainsbury_url = "https://www.sainsburys.co.uk"

        super().__init__(sainsbury_url)

    def shop(self, username, password):
        self._open_sainsbury()
        self._to_login()
        self._login(username, password)
        self._search_item("tomato")
        item_options = self._find_item_elements()
        print(len(item_options))
        selected_item = self._select_item(item_options)
        self._get_item_details(selected_item)
        self._clear_search("tomato")
        self._search_item("ice cream")
        item_options = self._find_item_elements()
        selected_item = self._select_item(item_options)
        self._get_item_details(selected_item)

        return selected_item



    def _open_sainsbury(self):
        self._open_driver()
        self._open_url()

        # wait a second for page to load
        time.sleep(1)
        self._accept_cookies()

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
        self._accept_cookies()

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
        except (NoSuchElementException, TimeoutException):
            pass

    def _search_item(self, item):
        print("Searching for " + item)
        search = self.driver.find_element_by_id("search-bar-input")
        search.send_keys(item)
        search = self.driver.find_element_by_xpath(
            "//button[@class='search-bar__button']"
        )
        search.click()
        time.sleep(2)

    def _find_item_elements(self):
        try:
            item_options = self.driver.find_elements_by_xpath(
                 "//div[@class='ln-c-card pt']"
             )
            print(len(item_options))
            # for now, select the first 5 options - TODO make this user selected
            if len(item_options) > 5:
                item_options = [e for i, e in enumerate(item_options) if i < 5]

        except NoSuchElementException:
            item_options = None

        return item_options

    @staticmethod
    def _select_item(item_options):
        # if we have 0 or 1 options, no need to search for favourites
        if item_options is None:
            print("Unable to find item")
            return None
        elif len(item_options) == 1:
            return item_options[0]

        fav = False
        # otherwise, look for a favourite item
        for item in item_options:
            try:
                item.find_element_by_xpath("//button[@class='pt__icons__fav']")
                selected_item = item
                fav = True
                break
            except NoSuchElementException:
                continue

        # if we don't find a favourite, then select the first
        if not fav:
            selected_item = item_options[0]

        return selected_item

    def _add_item():
        pass

    @staticmethod
    def _get_item_details(selected_item):
        info = selected_item.find_element_by_xpath("//a[@class='pt__link']")
        print(info.get_attribute("innerHTML"))

    def _clear_search(self, item):
        search = self.driver.find_element_by_id("search-bar-input")

        # https://stackoverflow.com/questions/7732125/clear-text-from-textarea-with-selenium
        # methods using .clear() or .sendKeys(Keys.CONTROL + "a") didn't work
        for i in range(len(item)):
            search.send_keys(Keys.BACK_SPACE)

if __name__ == "__main__":
    with open("/Users/david_zhang/dz_home/work/data_sci/autogroceries/credentials.txt") as file:
        credentials = file.readlines()
    sb = SainsburyShopper()
    options = sb.shop(credentials[0], credentials[1])
