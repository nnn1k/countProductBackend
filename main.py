import uvicorn

from app.settings import settings
from app.base_router import backend_router_v1
from app.utils.create_fastapi_app import create_app

app = create_app()

app.include_router(backend_router_v1)

if __name__ == '__main__':
    uvicorn.run(
        app,
        host=settings.run.host,
        port=settings.run.port,
        access_log=False
    )
