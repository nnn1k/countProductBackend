from loguru import logger
from fastapi import status
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
