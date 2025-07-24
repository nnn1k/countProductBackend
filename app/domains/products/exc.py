from fastapi import HTTPException
from starlette import status

bad_product_name_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad product name",
)
product_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product not found",
)
