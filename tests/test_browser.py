from autoceries.browser import SainsburyBrowser

sb = SainsburyBrowser()


def test_sainsbury_browser():
    assert sb.url == "https://www.sainsburys.co.uk"