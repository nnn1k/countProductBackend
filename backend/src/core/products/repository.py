from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
