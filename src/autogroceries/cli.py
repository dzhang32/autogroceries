import os
from pathlib import Path

import click
from dotenv import load_dotenv

from autogroceries.exceptions import MissingCredentialsError
from autogroceries.shopper.sainsburys import SainsburysShopper
from autogroceries.shopper.waitrose import WaitroseShopper

SHOPPERS = {
    "sainsburys": SainsburysShopper,
    "waitrose": WaitroseShopper,
}


@click.command(
    help="""
    Automate your grocery shopping using playwright.

    Please set the [STORE]_USERNAME and [STORE]_PASSWORD in a .env file in the same
    directory you run autogroceries. Replace [STORE] with the store name in caps
    e.g. SAINSBURYS_USERNAME.
    """
)
@click.option(
    "--store",
    type=click.Choice(SHOPPERS.keys()),
    required=True,
    help="The store to shop at.",
)
@click.option(
    "--ingredients-path",
    type=click.Path(exists=True, path_type=Path),
    required=True,
    help="Path to csv file (without header) detailing ingredients. "
    "Each line should in format 'ingredient,quantity' e.g. 'eggs,2'.",
)
@click.option(
    "--log-path",
    type=click.Path(path_type=Path),
    required=False,
    help="If provided, will output shopping log to this path.",
)
def autogroceries_cli(
    store: str, ingredients_path: Path, log_path: Path | None
) -> None:
    load_dotenv()

    # Get store credentials from environment variables.
    store_username = f"{store.upper()}_USERNAME"
    store_password = f"{store.upper()}_PASSWORD"
    username = os.getenv(store_username)
    password = os.getenv(store_password)

    if not username or not password:
        raise MissingCredentialsError(
            f"{store_username} and {store_password} must be set as environment variables."
        )

    shopper = SHOPPERS[store](
        username=username,
        password=password,
        log_path=log_path,
    )

    shopper.shop(read_ingredients(ingredients_path))


def read_ingredients(ingredients_path: Path) -> dict[str, int]:
    """
    Read ingredients from a csv file.

    Args:
        ingredients_path: Path to csv file (without header) detailing ingredients. Each
            line should in format 'ingredient,quantity' e.g. 'eggs,2'.

    Returns:
        Keys are the ingredients to add to the basket and values are the desired
        quantity of each ingredient.
    """
    ingredients = {}

    with open(ingredients_path, "r") as ingredients_file:
        for ingredient_quantity in ingredients_file:
            ingredient, quantity = ingredient_quantity.strip().split(",")
            ingredients[ingredient] = int(quantity)

    return ingredients
