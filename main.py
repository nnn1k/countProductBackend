import uvicorn

from backend.src.config.settings import settings
from configure_fastapi_app import config_app
from create_fastapi_app import create_app

app = config_app(create_app())

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port
    )
