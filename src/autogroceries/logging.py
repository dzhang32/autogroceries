import logging
from pathlib import Path


def setup_logger(log_path: Path | None = None) -> logging.Logger:
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

    if log_path:
        # Create directory in log_path if it does not exist.
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    return logging.getLogger(__name__)
