import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """
    Load credentials as environment variables from a .env file.
    """
    load_dotenv()
