from fastapi import FastAPI

from backend.src.config.add_cors import setup_cors
from backend.src.config.add_handlers import global_exception_handler, log_requests

from backend.api.routers.base import backend_router
from backend.src.lib.utils import check_platform
from backend.src.services.rebuild import rebuild_schemas


def create_app() -> FastAPI:
    app = FastAPI()
    app.exception_handler(Exception)(global_exception_handler)
    app.middleware("http")(log_requests)
    setup_cors(app)

    app.include_router(backend_router)

    rebuild_schemas()
    check_platform()

    return app
