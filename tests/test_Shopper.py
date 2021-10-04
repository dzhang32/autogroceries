import pytest
from autogroceries.shopper import Shopper
from selenium.common.exceptions import InvalidSessionIdException

# TODO: check whether I should use @pytest.fixture instead here
b = Shopper("https://www.sainsburys.co.uk", ["tomato", "lemon"])


def test_default_shopper():
    assert b.url == "https://www.sainsburys.co.uk"
    assert b.headless == False
    assert b.items == ["tomato", "lemon"]
    assert b.n_items == [1, 1]
    assert b.driver is None


def test_check_headless_catches_user_input_errors():
    with pytest.raises(TypeError, match="headless must be a boolean"):
        b._check_headless("not_a_bool")


def test_set_headless():
    b.headless = True
    assert b.headless == True


def test_check_items_catches_user_input_errors():
    with pytest.raises(TypeError, match="items must be a list"):
        b._check_items(1)

    with pytest.raises(TypeError, match="items must be a list of str elements"):
        b._check_items([1])


def test_check_n_items_catches_user_input_errors():
    with pytest.raises(TypeError, match="n_items must be a list"):
        b._check_n_items(b.items, 1)

    with pytest.raises(TypeError, match="n_items must be a list of int"):
        b._check_n_items(b.items, ["str"])

    with pytest.raises(ValueError, match="length of n_items and items"):
        b.n_items = [1, 2, 3]


def test_set_n_items():
    b.n_items = [1, 2]
    assert b.n_items == [1, 2]


def test_open_url_fails_when_driver_not_open():
    with pytest.raises(ValueError, match="driver has not yet been opened"):
        b._open_url()


def test_open_url_fails_works_after_open_driver():
    b._open_driver()
    b._open_url()
    assert b.driver.title == "Sainsbury’s"


def test_close_driver():
    # close the headless browser, could be changed to @pytest.fixture?
    b.close_driver()

    with pytest.raises(InvalidSessionIdException):
        b.driver.title
