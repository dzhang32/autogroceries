import os

from autogroceries.shopper import SainsburysShopper


def test_shopper():
    shopper = SainsburysShopper(
        username=os.getenv("SAINSBURYS_USERNAME"),
        password=os.getenv("SAINSBURYS_PASSWORD"),
    )
    shopper.shop(headless=False)
