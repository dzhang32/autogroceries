import pytest
import sys
from autogroceries.shopper import Shopper
from selenium.common.exceptions import InvalidSessionIdException

# TODO: check whether I should use @pytest.fixture instead here
shopper = Shopper("https://www.sainsburys.co.uk", ["tomato", "lemon"])


def test_default_shopper():
    assert shopper.url == "https://www.sainsburys.co.uk"
    assert shopper.headless == False
    assert shopper.items == ["tomato", "lemon"]
    assert shopper.n_items == [1, 1]
    assert shopper.driver is None


def test_check_headless_catches_user_input_errors():
    with pytest.raises(TypeError, match="headless must be a boolean"):
        shopper._check_headless("not_a_bool")


def test_set_headless():
    shopper.headless = True
    assert shopper.headless == True


def test_check_items_catches_user_input_errors():
    with pytest.raises(TypeError, match="items must be a list"):
        shopper._check_items(1)

    with pytest.raises(TypeError, match="items must be a list of str elements"):
        shopper._check_items([1])


def test_check_n_items_catches_user_input_errors():
    with pytest.raises(TypeError, match="n_items must be a list"):
        shopper._check_n_items(shopper.items, 1)

    with pytest.raises(TypeError, match="n_items must be a list of int"):
        shopper._check_n_items(shopper.items, ["str"])

    with pytest.raises(ValueError, match="length of n_items and items"):
        shopper.n_items = [1, 2, 3]


def test_set_n_items():
    shopper.n_items = [1, 2]
    assert shopper.n_items == [1, 2]


def test_open_url_fails_when_driver_not_open():
    with pytest.raises(ValueError, match="driver has not yet been opened"):
        shopper._open_url()

@pytest.mark.skipif(sys.platform == "linux", reason="skip selenium test on GHA")
def test_open_url_fails_works_after_open_driver():
    # TODO - figure out how to test selenium on GHA
    shopper._open_driver()
    shopper._open_url()
    assert shopper.driver.title == "Sainsbury’s"

@pytest.mark.skipif(sys.platform == "linux", reason="skip selenium test on GHA")
def test_close_driver():
    # close the headless browser, could be changed to @pytest.fixture?
    shopper.close_driver()

    with pytest.raises(InvalidSessionIdException):
        shopper.driver.title
