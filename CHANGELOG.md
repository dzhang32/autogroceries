# Changelog

## v2.0.0 (07/09/2025)

- Refactor to use modern python practices:

    - `uv` for python packaging.
    - Revamp CI workflow.
    - Replace `selenium` with `Playwright`.
    - Add use `ruff` and `mypy` for pre-commit hooks and add type hints.
    - Improve code design and structure.
    - Add logging, docs and docstrings.

## v1.0.3 (01/08/2022)

- Update to depend on python version 3.10. This resolves some security issues in dependencies and permits use of the latest `selenium`/`webdriver` versions.

## v1.0.2 (18/06/2022)

- Fix problem obtaining the product elements using `_get_products`.

## v1.0.1 (26/03/2022)

- Change output of `SainsburysShopper` to `pandas.DataFrame()`.

## v1.0.0 (24/03/2022)

- First release of `autogroceries`!
