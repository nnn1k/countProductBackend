from fastapi import FastAPI

from backend.api.routers.base import backend_router
from backend.src.config.async_helper import check_platform
from backend.src.config.logger_config.db_logs import db_logger
from backend.src.core.rebuild import rebuild_schemas


def config_app(app: FastAPI) -> FastAPI:
    app.include_router(backend_router)

    rebuild_schemas()
    check_platform()
    db_logger()

    return app
