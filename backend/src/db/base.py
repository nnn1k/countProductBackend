from typing import Annotated

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import mapped_column, DeclarativeBase

from backend.src.config.settings import settings

engine = create_async_engine(
    url=settings.db.url
)
session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

int_pk = Annotated[
    int,
    mapped_column(primary_key=True)
]

created_at = Annotated[
    int,
    mapped_column(
        server_default=text("EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::int"),
    )
]

updated_at = Annotated[
    int,
    mapped_column(
        server_default=text("EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::int"),
        onupdate=text("EXTRACT(EPOCH FROM CURRENT_TIMESTAMP)::int"),
    )
]


class Base(DeclarativeBase):
    ...



