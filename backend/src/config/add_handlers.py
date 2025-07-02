import time

from fastapi import status, Request
from fastapi.responses import JSONResponse

from backend.src.config.logger_config import logger


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Произошла ошибка на сервере.",
            'error': exc.args,
        }
    )


async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info('--------------')
    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"

    if response.status_code == 307 and "location" in response.headers:
        location = response.headers["location"]
        if location.startswith("http://"):
            response.headers["location"] = location.replace("http://", "https://")

    logger.info(
        f"\nmethod={request.method}"
        f"\npath={request.url.path}"
        f"\nstatus_code={response.status_code}"
        f"\nprocessed_in={formatted_process_time}ms"
    )

    logger.info('--------------\n')
    return response
