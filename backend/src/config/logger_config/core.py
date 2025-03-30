import os

from loguru import logger

log_directory = os.path.join(os.getcwd(), "backend/logs")

logger.level('DATABASE', no=25, color='<cyan>')
logger.level('TIME', no=26, color='<yellow>')

os.makedirs(log_directory, exist_ok=True)

logger.add(
    os.path.join(log_directory, "database.log"),
    level="DATABASE"
)

logger.add(
    os.path.join(log_directory, "time.log"),
    level="TIME",
)

logger.add(
    os.path.join(log_directory, "info.log"),
    level="INFO",
)

logger.add(
    os.path.join(log_directory, "error.log"),
    level="ERROR",
)

