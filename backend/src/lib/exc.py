from fastapi import HTTPException, status

incorrect_login_or_password_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
)

user_is_exist_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User is exist",
)

invalid_token_exc = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid token (refresh)",
)

bad_storage_name_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad storage name",
)

bad_generation_code_exc = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Bad generation code",
)

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

storage_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Storage not found",
)

bad_category_name_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad category name",
)

bad_product_name_exc = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Bad product name",
)
product_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Product not found",
)

category_not_found_exc = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Category not found",
)
