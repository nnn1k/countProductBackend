import time

from loguru import logger
from fastapi.requests import Request


async def log_time_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    if request.url.path.startswith("/api"):
        logger.info(
            f"{request.method} {request.url.path} - \n"
            f"Статус: {response.status_code} - Время обработки: {duration:.4f} секунд\n"
        )

    return response
