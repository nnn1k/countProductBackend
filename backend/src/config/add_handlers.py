import time

from fastapi import status, Request
from fastapi.responses import JSONResponse

from backend.src.config.log_config import logger


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

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}"

    logger.info(
        f"\n method={request.method}"
        f"\n path={request.url.path}"
        f"\n status_code={response.status_code}"
        f"\n processed_in={formatted_process_time}ms"
    )

    return response
