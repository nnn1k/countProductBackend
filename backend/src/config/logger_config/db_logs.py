from sqlalchemy import event

from backend.src.config.logger_config.core import logger
from backend.src.db.core import engine


def log_queries(conn, cursor, statement, parameters, context, executemany):
    logger.log('DATABASE', f"Executing: {statement} | Params: {parameters}\n")


def db_logger():
    event.listen(engine.sync_engine, 'before_cursor_execute', log_queries)

