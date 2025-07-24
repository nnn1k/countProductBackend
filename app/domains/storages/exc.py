from fastapi import HTTPException
from starlette import status

bad_storage_name_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad storage name",
)
bad_generation_code_exc = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Bad generation code",
)
storage_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Storage not found",
)
