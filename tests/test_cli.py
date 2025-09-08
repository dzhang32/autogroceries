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
    reason="Sainsburys website can't be tested in headless mode.",
)
def test_autogroceries_cli(ingredients_path: Path, tmp_path: Path) -> None:
    """
    Test the autogroceries CLI works correctly.
    """
    runner = CliRunner()
    result = runner.invoke(
        autogroceries_cli,
        [
            "--store",
            "sainsburys",
            "--ingredients-path",
            str(ingredients_path),
            "--log-path",
            str(tmp_path / "test_dir" / "test.log"),
        ],
    )

    assert result.exit_code == 0


def test_read_ingredients(ingredients_path: Path) -> None:
    """
    Test that ingredients are read correctly from a csv file.
    """
    assert read_ingredients(ingredients_path) == {"eggs": 2, "milk": 1}
