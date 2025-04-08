import time

from fastapi import HTTPException, status
from loguru import logger
from fastapi.requests import Request
from fastapi.responses import JSONResponse


async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Необработанное исключение: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Произошла ошибка на сервере.",
            'error': exc.args,
        }
    )


async def log_time_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    if request.url.path.startswith("/api"):
        logger.info(
            f"{request.method} {request.url.path} - \n"
            f"Статус: {response.status_code} - Время обработки: {duration:.4f} секунд\n")

    return response
