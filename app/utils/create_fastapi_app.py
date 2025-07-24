from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.utils.add_cors import setup_cors
from app.utils.add_handlers import register_exceptions_handler, register_logger_middleware

from app.utils.utils import check_platform
from app.utils.rebuild import rebuild_schemas


def create_app() -> FastAPI:
    check_platform()
    rebuild_schemas()

    app = FastAPI(default_response_class=ORJSONResponse)

    register_exceptions_handler(app)
    register_logger_middleware(app)
    setup_cors(app)

    return app
