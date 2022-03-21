## autogroceries

<!-- badges: start -->

[![Lifecycle:
experimental](https://img.shields.io/badge/lifecycle-experimental-orange.svg)](https://lifecycle.r-lib.org/articles/stages.html#experimental)
[![ci](https://github.com/dzhang32/autogroceries/workflows/test-deploy-package/badge.svg)](https://github.com/dzhang32/autogroceries/actions)
[![Codecov test
coverage](https://codecov.io/gh/dzhang32/autogroceries/branch/master/graph/badge.svg)](https://codecov.io/gh/dzhang32/autogroceries?branch=master)
<!-- badges: end -->

The goal of `autogroceries` is to automate your weekly grocery shop (from Sainsbury's).

## Installation

autorecipes exists purely for personal use and is no longer under active development. If you’d like to install the development version from `pypi` you can use the following:

```bash
pip install autogroceries
```

## Usage

`autogroceries` uses [Selenium](https://selenium-python.readthedocs.io) to interface with the Sainsbury's website, automatically filling your cart with a user-inputted list of ingredients.

The below illustrates the minimal config required to run `autogroceries`. For a more detailed tutorial please see the vignette.

```python
from autogroceries.shopper import SainsburysShopper

ingreds = ["tomatoes", "lemon"]
n_ingreds = [1, 2]
sb = SainsburysShopper(ingreds, n_ingreds)

# SainsburysShopper requires the input of a Sainsbury's grocery account 
# username/email and password
# it's recommended to load these from a separate file
# rather than inputting your credentials directly
shopping_list = sb.shop("UN", "PW")
```

## Credits

`autogroceries` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
