from backend.src.config.logger_config import logger
from backend.src.db.base import session_factory


async def get_db():
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
            logger.info("\ncommit")
        except Exception as e:
            await session.rollback()
            logger.info(f'\nRollback due to: {str(e)}')
            raise e
        finally:
            await session.close()
