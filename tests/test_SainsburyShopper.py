from autogroceries.shopper import SainsburyShopper

sb = SainsburyShopper(["tomato", "lemon"], [1, 2])


def test_default_sainsbury_shopper():
    assert sb.url == "https://www.sainsburys.co.uk"
    assert sb.headless == False
    assert sb.items == ["tomato", "lemon"]
    assert sb.n_items == [1, 2]
    assert sb.driver is None


def test_default_sainsbury_shopper():
    sb._open_sainsbury()
