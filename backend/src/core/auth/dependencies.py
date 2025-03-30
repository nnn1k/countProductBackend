from fastapi import Depends, Cookie
from jwt import ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import Response

from backend.src.core.users.dependencies import get_user_service
from backend.src.core.users.service import UserService
from backend.src.core.auth.repository import AuthRepository
from backend.src.core.auth.service import AuthService
from backend.src.db.dependencies import get_db
from backend.src.core.users.schemas import UserSchema
from backend.src.lib.classes.AuthJWT import jwt_token
from backend.src.lib.const import ACCESS_TOKEN, REFRESH_TOKEN
from backend.src.lib.exc import invalid_token_exc


def get_auth_repo(
        session: AsyncSession = Depends(get_db)
) -> AuthRepository:
    return AuthRepository(session)


def get_auth_service(
        auth_repo: AuthRepository = Depends(get_auth_repo)
) -> AuthService:
    return AuthService(repo=auth_repo)


async def get_user_by_token(
        access_token=Cookie(None, include_in_schema=False),
        refresh_token=Cookie(None, include_in_schema=False),
        response: Response = None,
        service: UserService = Depends(get_user_service)
) -> UserSchema:
    if access_token is None:
        user_id = check_refresh_token(refresh_token, response)
    else:
        try:
            user_id = jwt_token.decode_jwt(token=access_token).get("sub")
        except ExpiredSignatureError:
            user_id = check_refresh_token(refresh_token, response)
    if not user_id:
        raise invalid_token_exc
    return await service.get_user(id=int(user_id))


def check_refresh_token(refresh_token, response) -> int:
    if refresh_token is None:
        raise invalid_token_exc
    try:
        new_access_token, new_refresh_token = jwt_token.token_refresh(refresh_token)
        if new_access_token is None or new_refresh_token is None:
            raise invalid_token_exc

        response.set_cookie(key=ACCESS_TOKEN, value=new_access_token)
        response.set_cookie(key=REFRESH_TOKEN, value=new_refresh_token)
        user_id = jwt_token.decode_jwt(token=new_access_token).get("sub")
        return user_id
    except Exception:
        raise invalid_token_exc
