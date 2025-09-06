import logging
from pathlib import Path


def setup_logger(log_path: Path | None = None) -> logging.Logger:
    """
    Setup logger.

    Args:
        log_path: Optional. If provided, will output log to this path.

    Returns:
        Logger with the desired configuration.
    """
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    root_logger = logging.getLogger()

    if log_path:
        # Create directory in log_path if it does not exist.
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)

    root_logger.setLevel(logging.INFO)

    return logging.getLogger(__name__)
