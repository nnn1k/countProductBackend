from fastapi import FastAPI

from backend.src.config.add_cors import setup_cors
from backend.src.config.logger_config.http_logs import log_time_requests
from backend.src.config.add_exception_handler import global_exception_handler


def create_app() -> FastAPI:
    app = FastAPI()
    app.exception_handler(Exception)(global_exception_handler)
    app.middleware("http")(log_time_requests)
    setup_cors(app)

    return app
