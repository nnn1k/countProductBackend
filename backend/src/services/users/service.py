from backend.src.services.users.repository import UserRepository
from backend.src.services.users.schemas import UserSchemaRel, UserSchema


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_user(self, **kwargs) -> UserSchema:
        user = await self.user_repo.get_user(**kwargs)
        return UserSchema.model_validate(user)

    async def get_user_rel(self, **kwargs) -> UserSchemaRel:
        user = await self.user_repo.get_user(rel=True, **kwargs)
        return UserSchemaRel.model_validate(user)
