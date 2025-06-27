import uvicorn

from backend.src.config.settings import settings

from create_fastapi_app import create_app

app = create_app()

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        access_log=False
    )
