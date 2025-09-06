import os

import pytest

from autogroceries.shopper.sainsburys import SainsburysShopper


# GHA autosets GITHUB_ACTIONS env var to true.
@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS") == "true",
    reason="Sainsburys website can't be tested in headless mode.",
)
def test_sainsburys_shopper():
    """
    Test that the Sainsbury's shopper works correctly.
    """
    shopper = SainsburysShopper(
        username=os.getenv("SAINSBURYS_USERNAME"),
        password=os.getenv("SAINSBURYS_PASSWORD"),
    )
    shopper.shop({"milk": 1, "egg": 2, "not_a_food": 2})
