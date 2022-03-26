from autogroceries.shopper import Shopper
from autogroceries.utils import pause
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import pandas as pd


class SainsburysShopper(Shopper):
    """Automates grocery shopping from the Sainsbury's website

    A SainsburysShopper object contains methods to open, login to, search items
    within and add products to a user's cart from the Sainsbury's website.

    Parameters
    ----------
    items : list
        List of items to search for and add to cart.
    n_items : list, default None
        List of equal length to items, determining the number of each item to
        order. If left as None, will assume user desires 1 of each item.

    Examples
    --------
    >>> ss = SainsburysShopper(['tomato', 'lemon'], [1, 2])
    >>> ss.shop("UN", "PW")
    """

    def __init__(self, items, n_items=None):
        sainsburys_url = "https://www.sainsburys.co.uk"

        super().__init__(sainsburys_url, items, n_items)

    def shop(self, username, password, file=None):
        """Automatically fill your Sainsbury's cart with selected items

        Search the Sainsbury's grocery products for each item in turn, then add
        the products found to the user's cart.


        Parameters
        ----------
        username : str
            Username for Sainsbury's grocery account.
        password : str
            Password for Sainsbury's grocery account.
        file : None or str, default None
            If entered, must be a path to save the names of the items searched
            and products added to the cart as a csv.

        Returns
        -------
        dict
            Keys as the names of the items searched and values as the names of
            the products added to cart.
        """

        self._open_sainsburys()
        self._to_login()
        self._login(username, password)
        added_products = self._add_products_to_cart()
        items_products = self._get_items_products(added_products, file)

        return items_products

    def _add_products_to_cart(self):
        """Add products to the cart

        Loops across the items, searches their name and adds corresponding
        product results to user's Sainsbury's cart. A 'Not found' str is used to
        mark items that did not have corresponding product found in the
        Sainsbury's store.

        Returns
        -------
        list
            The names of the Sainsbury's products that were added to the cart,
            corresponding to each searched item.
        """

        added_products = list()
        for n, item in zip(self.n_items, self.items):
            self._search_item(item)
            self._check_popup()
            products = self._get_products()
            if products is None:
                added_products.append("Not found")
            else:
                selected_product = self._select_item(products)
                product_name = self._get_product_name(selected_product)
                added_products.append(product_name)
                self._add_product(selected_product, n)

            self._clear_search(item)

        return added_products

    def _open_sainsburys(self):
        """Opens a Selenium webdriver and navigate to the Sainsbury's website

        Initialises the self.driver attribute, required for all of the remaining
        SainsburysShopper methods.
        """

        self._open_driver()
        self._open_url()

        # wait a second for page to load
        self._accept_cookies()

    @pause
    def _accept_cookies(self):
        """Click accept all cookies

        Accepts cookies on the Sainsbury's website, to avoid cookies popup
        masking other required elements on the page (e.g. the search bar).
        """

        wait = WebDriverWait(self.driver, 3)
        accept_box = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Accept All Cookies']")
            )
        )

        # https://sqa.stackexchange.com/questions/40678/using-python-selenium-not-able-to-perform-click-operation
        # required otherwise obtain ElementClickInterceptedException
        self.driver.execute_script("arguments[0].click();", accept_box)

    @pause
    def _to_login(self):
        """Navigate to the Sainsbury's grocery account login page"""

        login = self.driver.find_element_by_xpath("//span[text()='Log in']")
        login.click()
        groceries = self.driver.find_element_by_xpath("//a[text()='Groceries account']")
        groceries.click()

    @pause
    def _login(self, username, password):
        """Login to the Sainsbury's website

        Sainsbury's does have a two-factor authentication system in place.
        When logging in for the first time in a while, users are required to
        enter a code (obtained via email) to verify their identify. This can
        cause issues with the _login method. Currently, the only solution is to
        first login and complete the two-factor authentication manually before
        running .shop().

        Parameters
        ----------
        username : str
            Username for Sainsbury's grocery account.
        password : str
            Password for Sainsbury's grocery account.
        """

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
            cont = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Continue']"))
            )
            cont.click()
        except (NoSuchElementException, TimeoutException):
            pass

    @pause
    def _search_item(self, item):
        """Search for an item

        Parameters
        ----------
        item : str
            Name of the current item to be searched.
        """

        print("Searching for " + item)
        search = self.driver.find_element_by_id("search-bar-input")
        search.send_keys(item)
        search = self.driver.find_element_by_xpath(
            "//button[@class='search-bar__button']"
        )
        search.click()

    def _check_popup(self):
        """Click no Sainsbury's popup

        The Sainsbury's website periodically has a popup that offers users a
        chance to enter a competition by filling a survey. This overlays the
        site and obscures some of the elements required by SainsburysShopper.
        This method clicks the 'no' option on the popup.
        """

        try:
            popup = self.driver.find_element_by_xpath(
                "//a[@id='smg-etr-invitation-no']"
            )
            popup.click()
        except NoSuchElementException:
            pass

    def _get_products(self):
        """Obtain products that result from searching an item

        Obtains the webelements that correspond to the Sainsbury's products
        found for the current searched item. As of now, this limits the number
        of products to the first 5, however there is scope to make this
        user-defined in future if needed.
        """

        try:
            # look for the 'Category' button panel
            # only appears once search has loaded
            wait = WebDriverWait(self.driver, 3)
            wait.until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        "//div[@class='product-filter__row--items "
                        + "skipto-content__focus']",
                    )
                )
            )
        except TimeoutException:
            return None

        products = self.driver.find_elements_by_xpath("//div[@class='ln-c-card pt']")

        # for now, select the first 5 options - TODO make this user selected
        if len(products) > 5:
            products = [e for i, e in enumerate(products) if i < 5]

        return products

    @staticmethod
    def _select_item(products):
        """Select the product to add to cart

        If there is more than 1 product found via the search, this function will
        select one to add to cart, by either picking a favourites or selecting
        the first product arbitrarily if no favourites are found.

        Parameters
        ----------
        products : list
            Contains webelements corresponding to the Sainsbury's products
            resulting from searching the current item.

        Returns
        -------
        selenium.webdriver.remote.webelement.WebElement
            The webelement corresponding to the chosen item to be added to cart.
        """

        # if we only have 1 option, no need to search for favourites
        if len(products) == 1:
            return products[0]

        # by default let's select the first item available
        selected_product = products[0]

        # then, let's look for a favourite item
        for product in products:
            try:
                # .// needed here, the . refers to ONLY search the current node
                # https://github.com/seleniumhq/selenium-google-code-issue-archive/issues/5819
                product.find_element_by_xpath(".//button[@class='pt__icons__fav']")
                selected_product = product
                break
            except NoSuchElementException:
                continue

        return selected_product

    @pause
    def _add_product(self, selected_product, n):
        """Add the selected item to the Sainsbury's cart

        Parameters
        ----------
        selected_product : selenium.webdriver.remote.webelement.WebElement
            The webelement corresponding to the selected product to be added to
            cart
        n : int
            The number of current item that should be added.
        """

        wait = WebDriverWait(selected_product, 2)

        try:
            # add button is not found if the item has been already added
            # this try/except allows us to add items already present in basket
            add = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//button[@data-test-id='add-button']")
                )
            )
            add.click()
            # take 1 away from n as we add 1
            n -= 1
        except TimeoutException:
            pass

        # if we still need to add more, click increment n times
        if n > 0:
            add_more = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, ".//button[@data-test-id='pt-button-inc']")
                )
            )

            for i in range(n):
                add_more.click()

    @staticmethod
    def _get_product_name(selected_product):
        """Obtain the name of the selected product

        Parameters
        ----------
        selected_product : selenium.WebElement
            The web element corresponding to the selected item to be added to
            cart.

        Returns
        -------
        str
            Name of the Sainsbury's product that has been added to cart.
        """

        # needs to look in the current node, hence prefix with "." in ".//"
        product_info = selected_product.find_element_by_xpath(".//a[@class='pt__link']")
        product_name = product_info.get_attribute("innerHTML")

        return product_name

    @pause
    def _clear_search(self, item):
        """Clear the search bar

        Parameters
        ----------
        item : str
            Name of the searched item, the length of which will determine the
            number of backspaces to send to the search box.
        """

        search = self.driver.find_element_by_id("search-bar-input")

        # https://stackoverflow.com/questions/7732125/clear-text-from-textarea-with-selenium
        # methods using .clear() or .sendKeys(Keys.CONTROL + "a") didn't work
        for i in range(len(item)):
            search.send_keys(Keys.BACK_SPACE)

    def _get_items_products(self, added_products, file):
        """Tidy (and save) the searched items and added products

        Creates a dictionary, with keys as the searched items and the values as
        the carted products. Then possibly save this as a csv, if the user has
        inputted a file path.

        Parameters
        ----------
        added_products : list
            The names of the Sainsbury's products that have been added to the
            cart, corresponding to each searched item.
        file : None or str
            If a str, should be the path to save the searched items/added
            products as a csv.

        Returns
        -------
        dict
            Keys as the searched items and the values as the carted products.
        """

        items_products = pd.DataFrame(
            {
                "item": self.items,
                "n_items": self.n_items,
                "added_product": added_products,
            }
        )

        if file is not None:
            items_products.to_csv(file)

        return items_products
