## autogroceries

<!-- badges: start -->

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
[![ci](https://github.com/dzhang32/autogroceries/workflows/test-deploy-package/badge.svg)](https://github.com/dzhang32/autogroceries/actions)
[![PyPI](https://img.shields.io/pypi/v/autogroceries.svg)](https://pypi.python.org/pypi)
<!-- badges: end -->

The goal of `autogroceries` is to automate your weekly grocery shop (from Sainsbury's).

## Installation

 `autogroceries` was developed for for personal use and is no longer under active development. You can install the development version from `pypi`:

```bash
pip install autogroceries
```

## Usage

`autogroceries` uses [Selenium](https://selenium-python.readthedocs.io) to interface with the Sainsbury's website, automatically filling your cart with an inputted list of ingredients.

The below illustrates the minimal config required to run `autogroceries`.

```python
from autogroceries.shopper import SainsburysShopper

ingreds = ["tomatoes", "lemon"]
n_ingreds = [1, 2]
sb = SainsburysShopper(ingreds, n_ingreds)

# SainsburysShopper needs Sainsbury's grocery account username/email and password
# for security, it's recommended to load these from a file
# rather than inputting your credentials directly
shopping_list = sb.shop("UN", "PW")
```

https://user-images.githubusercontent.com/32676710/173201096-95633b21-d023-439d-9d18-8d00d0e33c4a.mp4

## Credits

`autogroceries` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
