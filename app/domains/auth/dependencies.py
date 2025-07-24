from fastapi import Depends, Cookie
from jwt import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from app.utils.logger_config import logger
from app.domains.users.dependencies import get_user_service
from app.domains.users.service import UserService
from app.domains.auth.repository import AuthRepository
from app.domains.auth.service import AuthService
from app.database.dependencies import get_db
from app.domains.users.schemas import UserSchema
from app.utils.classes.AuthJWT import jwt_token

from app.domains.auth.exc import invalid_token_exc


def get_auth_repo(session: AsyncSession = Depends(get_db)) -> AuthRepository:
    return AuthRepository(session)


def get_auth_service(auth_repo: AuthRepository = Depends(get_auth_repo)) -> AuthService:
    return AuthService(repo=auth_repo)


async def get_user_by_token(
    access_token=Cookie(None, include_in_schema=False),
    refresh_token=Cookie(None, include_in_schema=False),
    response: Response = None,
    service: UserService = Depends(get_user_service),
) -> UserSchema:
    user_id: int | None = None
    if access_token:
        try:
            user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        except ExpiredSignatureError:
            logger.info("access token expired")

    if not user_id and refresh_token:
        try:

            token = jwt_token.token_refresh(refresh_token)
            if not token:
                raise invalid_token_exc

            user_id = jwt_token.decode_jwt(token=token.access_token).get("sub")
            if not user_id:
                raise invalid_token_exc

            response.set_cookie(key=jwt_token.ACCESS_TOKEN, value=token.access_token)
            response.set_cookie(key=jwt_token.REFRESH_TOKEN, value=token.refresh_token)

        except ExpiredSignatureError:
            raise invalid_token_exc

    return await service.get_user(id=int(user_id))
