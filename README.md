# autogroceries

[![test_deploy](https://github.com/dzhang32/autogroceries/actions/workflows/test_deploy.yml/badge.svg)](https://github.com/dzhang32/autogroceries/actions/workflows/test-deploy.yml)
[![pypi](https://img.shields.io/pypi/v/autogroceries.svg)](https://pypi.org/project/autogroceries/)

`autogroceries` simplifies grocery shopping from Sainsbury's by using [Playwright](https://playwright.dev/) to automate the addition of ingredients to your basket.

## Installation

I recommend using [uv](https://docs.astral.sh/uv/) to manage the python version, virtual environment and `autogroceries` installation:

```bash
uv venv --python 3.13
source .venv/bin/activate
uv pip install autogroceries
# Install Chromium browser binary required for playwright.
playwright install chromium
```

## Usage

`autogroceries` uses [Playwright](https://playwright.dev/) to interface with the Sainsbury's website, automatically filling your cart with an inputted list of ingredients.

The below demonstrates how to run `autogroceries`:

```python
from autogroceries.shopper.sainsburys import SainsburysShopper

ingredients = {"milk": 1, "egg": 2}

# Store credentials securely e.g. in environment variables (use python-dotenv).
shopper = SainsburysShopper(
        username=os.getenv("SAINSBURYS_USERNAME"),
        password=os.getenv("SAINSBURYS_PASSWORD"),
    )

shopper.shop(
    {"cereal": 1, "tomatoes": 1, "lemon": 2, "salad": 1, "grapefruit": 3}
    )
```

The video below demonstrates how `Playwright` automates grocery shopping when running the example code above:

<video src="https://user-images.githubusercontent.com/32676710/173201096-95633b21-d023-439d-9d18-8d00d0e33c4a.mp4" controls style="max-width: 100%; height: auto;">
  Your browser does not support the video tag.
</video>
