from backend.src.config.logger_config.core import logger


def log_queries(conn, cursor, statement, parameters, context, executemany):
    logger.log('DATABASE', f"Executing: {statement} | Params: {parameters}\n")



