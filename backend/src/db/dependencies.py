from backend.src.config.log_config import logger
from backend.src.db.base import session_factory


async def get_db():
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
            logger.debug("commit")
        except Exception as e:
            await session.rollback()
            logger.debug(f'Rollback due to: {str(e)}')
            raise e
        finally:
            await session.close()
