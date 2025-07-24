import datetime
from typing import Annotated

from sqlalchemy import text, TIMESTAMP, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped

from app.settings import settings

engine = create_async_engine(
    url=settings.db.url
)
session_factory = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

int_pk = Annotated[
    int,
    mapped_column(primary_key=True)
]

created_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now()
    )
]

updated_at = Annotated[
    datetime,
    mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
]


class Base(DeclarativeBase):
    ...
