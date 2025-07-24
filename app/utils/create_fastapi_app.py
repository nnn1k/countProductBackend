from fastapi import FastAPI

from app.utils.add_cors import setup_cors
from app.utils.add_handlers import global_exception_handler, log_requests

from app.base_router import backend_router
from app.utils.utils import check_platform
from app.utils.rebuild import rebuild_schemas


def create_app() -> FastAPI:
    check_platform()
    rebuild_schemas()

    app = FastAPI()
    app.exception_handler(Exception)(global_exception_handler)
    app.middleware("http")(log_requests)
    setup_cors(app)

    app.include_router(backend_router)

    return app
