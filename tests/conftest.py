from pathlib import Path

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Load credentials as environment variables from a .env file.
    """
    load_dotenv()


@pytest.fixture
def test_data_dir():
    """
    Fixture for the test data directory.
    """
    return Path(__file__).parent / "data"
