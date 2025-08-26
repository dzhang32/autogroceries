import os

from autogroceries.shopper.sainsburys import SainsburysShopper


def test_shopper():
    shopper = SainsburysShopper(
        username=os.getenv("SAINSBURYS_USERNAME"),
        password=os.getenv("SAINSBURYS_PASSWORD"),
    )
    shopper.shop()
