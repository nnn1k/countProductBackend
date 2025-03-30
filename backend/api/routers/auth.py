from fastapi import APIRouter, Depends, Response

from backend.api.response_schemas import UserSchemaResponse
from backend.src.core.auth.schemas import UserLogin, UserRegister
from backend.src.core.users.schemas import UserSchema
from backend.src.core.auth.service import AuthService
from backend.src.core.auth.dependencies import get_auth_service

router = APIRouter(
    tags=['auth'],
    prefix='/auth',
)


@router.post('/login', response_model=UserSchemaResponse, summary='Авторизация')
async def login_views(
        login_schema: UserLogin,
        response: Response,
        service: AuthService = Depends(get_auth_service),
):
    user = await service.get_user_by_login(login_schema=login_schema, response=response)
    return {'user': user}


@router.post('/register', response_model=UserSchema, summary='Регистрация')
async def register_views(
        register_schema: UserRegister,
        response: Response,
        service: AuthService = Depends(get_auth_service),
):
    user = await service.create_user(register_schema=register_schema, response=response)
    return {'user': user}
