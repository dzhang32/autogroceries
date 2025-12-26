# autogroceries

[![test_deploy](https://github.com/dzhang32/autogroceries/actions/workflows/test_deploy.yml/badge.svg)](https://github.com/dzhang32/autogroceries/actions/workflows/test_deploy.yml)
[![pypi](https://img.shields.io/pypi/v/autogroceries.svg)](https://pypi.org/project/autogroceries/)

`autogroceries` simplifies grocery shopping by using [Playwright](https://playwright.dev/) to automate the addition of ingredients to your basket.

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

`autogroceries` uses [Playwright](https://playwright.dev/) to interface with the Sainsbury's or Waitrose website, automatically filling your cart with an inputted list of ingredients.

`autogroceries` is designed to be used as a CLI tool, with a single command:

```bash
❯ autogroceries --help
Usage: autogroceries [OPTIONS]

  Automate your grocery shopping using playwright.

  Please set the [STORE]_USERNAME and [STORE]_PASSWORD in a .env file in the
  same directory you run autogroceries. Replace [STORE] with the store name in
  caps e.g. SAINSBURYS_USERNAME.

Options:
  --store [sainsburys|waitrose]  The store to shop at.  [required]
  --ingredients-path PATH        Path to csv file (without header) detailing
                                 ingredients. Each line should be in the
                                 format 'ingredient,quantity' e.g. 'eggs,2'.
                                 [required]
  --log-path PATH                If provided, will output shopping log to this
                                 path.
  --help                         Show this message and exit.
```

The `autogroceries` CLI expects a `.env` file in the same directory from where you execute the command. This `.env` will be loaded by [python-dotenv](https://pypi.org/project/python-dotenv/) and should define the "[STORE]_USERNAME" and "[STORE]_PASSWORD" variables, with "[STORE]" replaced by the name of the store in uppercase, for instance:

```bash
# .env
SAINSBURYS_USERNAME=your_username
SAINSBURYS_PASSWORD=your_password
```

## Demo: autogroceries in action

<video src="https://user-images.githubusercontent.com/32676710/173201096-95633b21-d023-439d-9d18-8d00d0e33c4a.mp4" controls style="max-width: 100%; height: auto;">
  Your browser does not support the video tag.
</video>

## Disclaimer

️`autogroceries` is developed for **educational use only**. Users are responsible for:

- Following website's `robots.txt` and Terms of Service.
- Using appropriate delays and respecting rate limits.
- Complying with applicable laws.
