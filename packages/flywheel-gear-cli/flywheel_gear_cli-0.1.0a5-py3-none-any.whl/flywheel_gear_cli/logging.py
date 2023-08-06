"""Logging module."""
import logging
import os
import time
from pathlib import Path

CACHE_DIRPATH = Path("~/.cache/flywheel").expanduser()

DEFAULT_CLI_LOG_PATH = CACHE_DIRPATH / "logs/cli.log"

LOG_FILE_PATH = Path(
    os.environ.get("FW_LOG_FILE_PATH", DEFAULT_CLI_LOG_PATH)
).expanduser()

LOG_FILE_DIRPATH = os.path.dirname(LOG_FILE_PATH)


def configure_logging(args):  # pragma: no cover
    """Logging config."""
    root = logging.getLogger()

    # Propagate all debug logging
    root.setLevel(logging.DEBUG)

    # Always log to cli log file (except when disabled)
    if os.environ.get("FW_DISABLE_LOG_FILE") != "1":
        log_path = LOG_FILE_PATH
        log_dir = os.path.dirname(log_path)
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)

        # Use GMT ISO date for logfile
        file_formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d %(levelname)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S",
        )
        file_formatter.converter = time.gmtime

        # Allow environment overrides for log size and backup count
        log_file_size = int(
            os.environ.get("FW_LOG_FILE_SIZE", "5242880")
        )  # Default is 5 MB
        log_file_backup_count = int(
            os.environ.get("FW_LOG_FILE_COUNT", "2")
        )  # Default is 2

        file_handler = logging.handlers.RotatingFileHandler(
            log_path, maxBytes=log_file_size, backupCount=log_file_backup_count
        )
        file_handler.setFormatter(file_formatter)
        root.addHandler(file_handler)

    # Control how much (if anything) goes to console
    console_log_level = logging.INFO
    if getattr(args, "quiet", False):
        console_log_level = logging.ERROR
    elif getattr(args, "debug", False):
        console_log_level = logging.DEBUG

    console_formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(console_log_level)
    root.addHandler(console_handler)

    # Finally, capture all warnings to the logging framework
    logging.captureWarnings(True)
