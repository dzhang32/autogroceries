from autogroceries.shopper import Shopper
from autogroceries.utils import pause
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import csv


class SainsburyShopper(Shopper):

    def __init__(self, items, n_items=None):
        sainsbury_url = "https://www.sainsburys.co.uk"

        super().__init__(sainsbury_url, items, n_items)

    def shop(self, username, password, save=None):
        self._open_sainsbury()
        self._to_login()
        self._login(username, password)
        added = self._add_items_to_cart()
        searched_added = self._get_searched_added(added, save)

        return searched_added

    def _add_items_to_cart(self):
        added = list()
        for n, item in zip(self.n_items, self.items):
            self._search_item(item)
            self._check_popup()
            item_options = self._find_item_elements()
            if item_options is None:
                added.append("Not found")
            else:
                selected_item = self._select_item(item_options)
                item_info = self._get_item_details(selected_item)
                added.append(item_info)
                self._add_item(selected_item, n)

            self._clear_search(item)

        return added

    def _open_sainsbury(self):
        self._open_driver()
        self._open_url()

        # wait a second for page to load
        self._accept_cookies()

    @pause
    def _accept_cookies(self):
        # wait for few seconds for the cookies box to become clickable
        wait = WebDriverWait(self.driver, 3)
        accept_box = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Accept All Cookies']"))
        )

        # https://sqa.stackexchange.com/questions/40678/using-python-selenium-not-able-to-perform-click-operation
        # required otherwise obtain ElementClickInterceptedException
        self.driver.execute_script("arguments[0].click();", accept_box)

    @pause
    def _to_login(self):
        login = self.driver.find_element_by_xpath("//span[text()='Log in']")
        login.click()
        groceries = self.driver.find_element_by_xpath(
            "//a[text()='Groceries account']"
        )
        groceries.click()

    @pause
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
        # currently must enter manually
        try:
            wait = WebDriverWait(self.driver, 3)
            cont = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Continue']"))
            )
            cont.click()
        except (NoSuchElementException, TimeoutException):
            pass

    @pause
    def _search_item(self, item):
        print("Searching for " + item)
        search = self.driver.find_element_by_id("search-bar-input")
        search.send_keys(item)
        search = self.driver.find_element_by_xpath(
            "//button[@class='search-bar__button']"
        )
        search.click()

    def _check_popup(self):
        try:
            popup = self.driver.find_element_by_xpath(
                "//a[@id='smg-etr-invitation-no']"
            )
            popup.click()
        except NoSuchElementException:
            pass

    def _find_item_elements(self):
        try:
            # look for the 'Category' button panel
            # only appears once search has loaded
            wait = WebDriverWait(self.driver, 3)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH,
                 "//div[@class='product-filter__row--items " +
                 "skipto-content__focus']"))
            )
        except TimeoutException:
            return None

        item_options = self.driver.find_elements_by_xpath(
                "//div[@class='ln-c-card pt']"
        )

        # for now, select the first 5 options - TODO make this user selected
        if len(item_options) > 5:
            item_options = [e for i, e in enumerate(item_options) if i < 5]

        return item_options

    @staticmethod
    def _select_item(item_options):
        # if we only have 1 option, no need to search for favourites
        if len(item_options) == 1:
            return item_options[0]

        # by default let's select the first item available
        selected_item = item_options[0]

        # then, let's look for a favourite item
        for item in item_options:
            try:
                # .// needed here, the . refers to ONLY search the current node
                # https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/5819
                item.find_element_by_xpath(".//button[@class='pt__icons__fav']")
                selected_item = item
                break
            except NoSuchElementException:
                continue

        return selected_item

    @pause
    def _add_item(self, selected_item, n):
        try:
            # add button is not found if the item has been already added
            # this try/except allows us to add items already present in basket
            add = selected_item.find_element_by_xpath(
                ".//button[@data-test-id='add-button']"
            )
            add.click()
            # take 1 away from n as we add 1
            n -= 1
        except NoSuchElementException:
            pass

        # if we still need to add more, click increment for n times
        if n > 0:
            wait = WebDriverWait(self.driver, 3)
            add_more = wait.until(EC.element_to_be_clickable(
                (By.XPATH, ".//button[@data-test-id='pt-button-inc']"))
            )

            for i in range(n):
                add_more.click()

    @staticmethod
    def _get_item_details(selected_item):
        # needs to look in the current node, hence prefix with "." in ".//"
        item_info = selected_item.find_element_by_xpath(
            ".//a[@class='pt__link']"
        )
        item_name = item_info.get_attribute("innerHTML")

        return item_name

    @pause
    def _clear_search(self, item):
        search = self.driver.find_element_by_id("search-bar-input")

        # https://stackoverflow.com/questions/7732125/clear-text-from-textarea-with-selenium
        # methods using .clear() or .sendKeys(Keys.CONTROL + "a") didn't work
        for i in range(len(item)):
            search.send_keys(Keys.BACK_SPACE)

    def _get_searched_added(self, added, save):
        searched_added = {key: value for key, value in zip(self.items, added)}

        if save is not None:
            with open(save, "w") as f:
                w = csv.writer(f)
                w.writerows(searched_added.items())

        return searched_added


if __name__ == "__main__":

    with open("/Users/david_zhang/dz_home/work/data_sci/autogroceries/credentials.txt") as file:
        credentials = file.readlines()
    with open("/Users/david_zhang/Downloads/shopping_list_dz_cjkg.txt") as file:
        shopping_list = file.readlines()

    ingredients = [j[:-3] for i, j in enumerate(shopping_list) if 3 > i > 0]
    number = [int(j.split("\t")[1][:-1]) for i, j in enumerate(shopping_list) if 3 > i > 0]
    sb = SainsburyShopper(ingredients, number)
    x = sb.shop(credentials[0], credentials[1], save="/Users/david_zhang/Downloads/shopping_list_added.txt")
    print(x)

