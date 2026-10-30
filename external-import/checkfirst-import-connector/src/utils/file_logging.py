"""Attach a host-visible file handler to the root logger for benchmarks."""

from __future__ import annotations

import logging
from pathlib import Path

from pycti.utils.opencti_logger import CustomJsonFormatter

# Match connectors-sdk / pycti JSON log line shape so file logs grep like stdout.
_PYCTI_LOG_RECORD_FORMAT = "%(timestamp)s %(level)s %(name)s %(message)s"


def attach_file_logging(log_file: str) -> Path:
    """Add a JSON ``FileHandler`` on the root logger if not already present.

    Call this **after** ``OpenCTIConnectorHelper`` / SDK logging setup: those
    steps may replace root handlers with ``force=True``.

    Args:
        log_file: Absolute or relative path inside the container (e.g.
            ``/var/log/checkfirst-connector/connector.log``).

    Returns:
        Resolved path of the log file.
    """
    path = Path(log_file).expanduser()
    path.parent.mkdir(parents=True, exist_ok=True)
    resolved = path.resolve()

    root = logging.getLogger()
    for handler in root.handlers:
        if (
            isinstance(handler, logging.FileHandler)
            and Path(handler.baseFilename).resolve() == resolved
        ):
            return resolved

    handler = logging.FileHandler(resolved)
    handler.setFormatter(CustomJsonFormatter(_PYCTI_LOG_RECORD_FORMAT))
    root.addHandler(handler)
    return resolved
