import logging
from logging import handlers
from pathlib import Path

base_directory = Path(__file__).resolve().parent.parent

log_format = logging.Formatter(
    "[%(asctime)s] %(levelname)s | %(funcName)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S:%MS",
)

logger = logging.getLogger("logger")
logger.setLevel(logging.DEBUG)
operator_handler = logging.handlers.SocketHandler("localhost", logging.handlers.DEFAULT_TCP_LOGGING_PORT)
operator_handler.setFormatter(log_format)
logger.addHandler(operator_handler)
