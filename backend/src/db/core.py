from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from backend.src.config.settings import settings

engine = create_async_engine(
    url=settings.db.url
)

session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)





