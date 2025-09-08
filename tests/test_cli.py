import os
from pathlib import Path

import pytest
from click.testing import CliRunner

from autogroceries.cli import autogroceries_cli, read_ingredients


@pytest.fixture
def ingredients_path(test_data_dir: Path) -> Path:
    """
    Path to the test ingredients csv file.
    """
    return test_data_dir / "test_cli" / "ingredients.csv"


# GHA autosets GITHUB_ACTIONS env var to true.
@pytest.mark.skipif(
    os.environ.get("GITHUB_ACTIONS") == "true",
    reason="Store websites can't be tested in headless mode.",
)
@pytest.mark.parametrize("store", ["sainsburys", "waitrose"])
def test_autogroceries_cli(store: str, ingredients_path: Path, tmp_path: Path) -> None:
    """
    Test the autogroceries CLI works correctly.
    """
    log_path = tmp_path / "test_dir" / "test.log"
    runner = CliRunner()
    result = runner.invoke(
        autogroceries_cli,
        [
            "--store",
            store,
            "--ingredients-path",
            str(ingredients_path),
            "--log-path",
            str(log_path),
        ],
    )

    assert result.exit_code == 0
    assert log_path.exists()


def test_read_ingredients(ingredients_path: Path) -> None:
    """
    Test that ingredients are read correctly from a csv file.
    """
    assert read_ingredients(ingredients_path) == {"eggs": 2, "milk": 1, "not_a_food": 2}
