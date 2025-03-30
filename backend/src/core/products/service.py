from backend.src.core.products.repository import ProductRepository


class ProductService:

    def __init__(self, product_repo: ProductRepository) -> None:
        self.product_repo = product_repo
