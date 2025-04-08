import uvicorn
from fastapi import FastAPI

from backend.api.routers.base import backend_router
from backend.src.config.add_cors import setup_cors
from backend.src.config.async_helper import check_platform
from backend.src.config.logger_config.db_logs import db_logger
from backend.src.config.logger_config.http_logs import global_exception_handler, log_time_requests
from backend.src.config.settings import settings
from backend.src.core.rebuild import rebuild_schemas

app = FastAPI()

setup_cors(app)
app.include_router(backend_router)


app.exception_handler(Exception)(global_exception_handler)
app.middleware("http")(log_time_requests)

rebuild_schemas()
check_platform()
db_logger()


if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port
    )



