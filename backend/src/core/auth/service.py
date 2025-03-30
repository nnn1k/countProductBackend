from fastapi import Response

from backend.src.lib.classes.AuthJWT import jwt_token
from backend.src.lib.const import ACCESS_TOKEN, REFRESH_TOKEN

from backend.src.core.auth.schemas import UserLogin, UserRegister

from backend.src.core.users.schemas import UserSchema
from backend.src.core.auth.repository import AuthRepository
from backend.src.lib.classes.HashPwd import HashPwd
from backend.src.lib.exc import incorrect_login_or_password_exc, user_is_exist_exc


class AuthService:

    def __init__(self, repo: AuthRepository):
        self.repo = repo

    async def get_user_by_login(
            self,
            login_schema: UserLogin,
            response: Response
    ) -> UserSchema:
        user = await self.repo.get_user_by_login(
            email=login_schema.login,
            nickname=login_schema.login
        )
        if not user:
            raise incorrect_login_or_password_exc
        if not HashPwd.validate_password(password=login_schema.password, hashed_password=user.password):
            raise incorrect_login_or_password_exc
        schema = UserSchema.model_validate(user)
        self._create_token(response=response, user=schema)
        return schema

    async def create_user(
            self,
            register_schema: UserRegister,
            response: Response
    ) -> UserSchema:
        check_user = await self.repo.get_user_by_login(
            email=register_schema.email,
            nickname=register_schema.nickname
        )
        if check_user:
            raise user_is_exist_exc
        user = await self.repo.register(
            nickname=register_schema.nickname,
            email=register_schema.email,
            hashed_password=HashPwd.hash_password(password=register_schema.password),
        )
        schema = UserSchema.model_validate(user)
        self._create_token(response=response, user=schema)
        return schema

    @staticmethod
    def _create_token(
            response: Response,
            user: UserSchema
    ) -> None:
        payload = {'sub': user.id}
        access_token = jwt_token.create_access_token(payload=payload)
        refresh_token = jwt_token.create_refresh_token(payload=payload)

        response.set_cookie(ACCESS_TOKEN, access_token, max_age=60 * 60 * 24 * 365)
        response.set_cookie(REFRESH_TOKEN, refresh_token, max_age=60 * 60 * 24 * 365)


