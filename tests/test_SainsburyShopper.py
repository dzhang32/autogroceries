from autogroceries.shopper import SainsburysShopper

sb = SainsburysShopper(["tomato", "lemon"], [1, 2])


def test_default_sainsburys_shopper():
    assert sb.url == "https://www.sainsburys.co.uk"
    assert sb.headless == False
    assert sb.items == ["tomato", "lemon"]
    assert sb.n_items == [1, 2]
    assert sb.driver is None


def test_default_sainsburys_shopper():
    sb._open_sainsbury()
