import logging

from sqlalchemy import event

from backend.src.db.base import engine


class DebugOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.DEBUG


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Устанавливаем минимальный уровень (чтобы DEBUG и INFO работали)


formatter = logging.Formatter('%(asctime)s %(message)s\n')

info_handler = logging.FileHandler("logs/info.log")
info_handler.setLevel(logging.INFO)  # Только INFO и выше
info_handler.setFormatter(formatter)


debug_handler = logging.FileHandler("logs/debug.log")
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(formatter)


debug_handler.addFilter(DebugOnlyFilter())

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(debug_handler)
logger.addHandler(console_handler)


def log_queries(conn, cursor, statement, parameters, context, executemany):
    logger.info(f"\nExecuting: {statement}"
                f"\nParams: {parameters}")


event.listen(engine.sync_engine, 'before_cursor_execute', log_queries)

