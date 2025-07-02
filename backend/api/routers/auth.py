from fastapi import APIRouter, Depends, Response

from backend.src.services.auth.schemas import UserLogin, UserRegister
from backend.src.services.users.schemas import UserSchemaResponse, UserSchema
from backend.src.services.auth.service import AuthService
from backend.src.services.auth.dependencies import get_auth_service

router = APIRouter(
    tags=["auth"],
    prefix="/auth",
)


@router.post("/login", response_model=UserSchemaResponse, summary="Авторизация")
async def login(
    login_schema: UserLogin,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.login(login_schema=login_schema, response=response)
    return {"user": user}


@router.post("/register", response_model=UserSchemaResponse, summary="Регистрация")
async def register(
    register_schema: UserRegister,
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    user = await service.register(register_schema=register_schema, response=response)
    return {"user": user}


@router.post("/logout", summary="Выход")
async def logout(
    response: Response,
    service: AuthService = Depends(get_auth_service),
):
    await service.logout(response=response)
    return {"msg": "user logged out"}
