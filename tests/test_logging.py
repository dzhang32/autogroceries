import logging
from pathlib import Path

import pytest

from autogroceries.logging import setup_logger


def test_setup_logger(caplog: pytest.LogCaptureFixture, tmp_path: Path) -> None:
    log_path = tmp_path / "test_dir" / "test.log"
    logger = setup_logger(log_path)

    assert isinstance(logger, logging.Logger)

    with caplog.at_level(logging.INFO):
        logger.info("test logging")

    assert log_path.exists()
    assert "test logging" in log_path.read_text()
