from fastapi import HTTPException
from starlette import status

category_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Category not found",
)
bad_category_name_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad category name",
)
