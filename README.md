# autogroceries

`autogroceries` simplifies grocery shopping from Sainsbury's by using [Playwright](https://playwright.dev/) to automate the addition of ingredients to your basket.

## Installation

I recommend using [uv](https://docs.astral.sh/uv/) to manage the python version, virtual environment and `autogroceries` installation:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install autogroceries
```

## Usage

`autogroceries` uses [Playwright](https://playwright.dev/) to interface with the Sainsbury's website, automatically filling your cart with an inputted list of ingredients. The below demonstrates how to run `autogroceries`:

```python
from autogroceries.shopper.sainsburys import SainsburysShopper

ingredients = {"milk": 1, "egg": 2}

# It is recommended to store your credentials in a secure .env file.
shopper = SainsburysShopper(
        username=os.getenv("SAINSBURYS_USERNAME"),
        password=os.getenv("SAINSBURYS_PASSWORD"),
    )

shopper.shop({"milk": 1, "egg": 2, "not_a_food": 2})
```

https://user-images.githubusercontent.com/32676710/173201096-95633b21-d023-439d-9d18-8d00d0e33c4a.mp4
