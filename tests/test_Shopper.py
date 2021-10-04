import pytest
from autogroceries.shopper import Shopper

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
    with pytest.raises(TypeError):
        b._check_items(1)

    with pytest.raises(TypeError):
        b._check_items([1])


def test_check_n_items_catches_user_input_errors():
    with pytest.raises(TypeError):
        b._check_n_items(1)

    with pytest.raises(TypeError):
        b._check_n_items([1])

    with pytest.raises(ValueError):
        b.n_items = [1, 2, 3]


def test_set_n_items():
    b.n_items = [1, 2]
    assert b.n_items == [1, 2]


def test_open_url_fails_when_driver_not_open():
    with pytest.raises(ValueError):
        b._open_url()


def test_open_url_fails_works_after_open_driver():
    b._open_driver()
    b._open_url()
    assert b.driver.title == "Sainsbury’s"
