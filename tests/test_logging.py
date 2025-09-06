import logging
from pathlib import Path

import pytest

from autogroceries.logging import setup_logger


def test_setup_logger(caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    """
    Test that the logger works as expected.
    """
    log_path = tmp_path / "test_dir" / "test.log"
    logger = setup_logger(log_path)

    assert isinstance(logger, logging.Logger)

    # Make sure logs printed in console.
    with caplog.at_level(logging.INFO):
        logger.info("test logging")

    # Make sure logs output to file.
    assert log_path.exists()
    assert "test logging" in log_path.read_text()
