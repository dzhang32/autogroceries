from autogroceries.shopper import Browser
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
b = Browser("https://www.sainsburys.co.uk", driver)


def test_browser():
    assert b .url == "https://www.sainsburys.co.uk"