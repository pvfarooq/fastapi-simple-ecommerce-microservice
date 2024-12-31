from core.db import session_local

from .crud import get_product_by_id


class StockService:
    def deduct_stock(self, product_id: int, quantity: int):
        with session_local() as session:
            product = get_product_by_id(session, product_id)
            product.stock = product.stock - quantity
            session.commit()
            session.close()
            print(f"Stock deducted for product {product_id}")
            return True
