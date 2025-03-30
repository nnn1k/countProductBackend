from typing import Annotated

from sqlalchemy import text
from sqlalchemy.orm import mapped_column, DeclarativeBase

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
