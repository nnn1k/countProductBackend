from fastapi import APIRouter, Depends

from app.domains.auth.dependencies import get_user_by_token
from app.domains.users.dependencies import get_user_service
from app.domains.users.schemas import UserSchemaRelResponse, UserSchema
from app.domains.users.service import UserService

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get('/me', response_model=UserSchemaRelResponse, summary='Получить информацию о себе')
async def get_me(
        user: UserSchema = Depends(get_user_by_token),
        service: UserService = Depends(get_user_service)
):
    user = await service.get_user_rel(id=user.id)
    return {'user': user}
