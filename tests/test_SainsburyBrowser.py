from autoceries.browser import SainsburyBrowser

sb = SainsburyBrowser()


def test_sb_default():
    assert sb.url == "https://www.sainsburys.co.uk"