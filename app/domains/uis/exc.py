from fastapi import HTTPException
from starlette import status

user_in_storage_exist_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User already exists in this storage",
)
user_in_storage_not_exist_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User does not exist in this storage",
)
user_is_not_owner_exc = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="User is not owner",
)
